import glucifer
import underworld as uw
from mpi4py import MPI
from .scaling import nonDimensionalize as nd
from .scaling import Dimensionalize
from .scaling import UnitRegistry as u
from . import rcParams
from .Underworld_extended import SwarmVariable
from scipy import interpolate
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


def _visugrid_drawing_object(Model, visugrid):

    m_minx, m_maxx = _get_minmax_coordinates_mesh(Model.mesh, 0)
    m_miny, m_maxy = _get_minmax_coordinates_mesh(Model.mesh, 1)
    model_domain = np.array([(m_minx, m_miny), (m_maxx, m_maxy)])

    v_minx, v_maxx = _get_minmax_coordinates_mesh(visugrid.mesh, 0)
    v_miny, v_maxy = _get_minmax_coordinates_mesh(visugrid.mesh, 1)
    # visugrid_domain = np.array([(v_minx, v_miny), (v_maxx, v_maxy)])

    minx = min(m_minx, v_minx)
    miny = min(m_miny, v_miny)
    maxx = max(m_maxx, v_maxx)
    maxy = max(m_maxy, v_maxy)

    full_domain = np.array([(minx, miny), (maxx, maxy)])
    bounds = full_domain[1] - full_domain[0]

    minx = (model_domain[0][0] - full_domain[0][0]) / bounds[0]
    maxx = 1 + (model_domain[1][0] - full_domain[1][0]) / bounds[0]
    miny = (model_domain[0][1] - full_domain[0][1]) / bounds[1]
    maxy = 1 + (model_domain[1][1] - full_domain[1][1]) / bounds[1]

    return (minx[0], maxx[0]), (miny[0], maxy[0])


def _get_minmax_coordinates_mesh(mesh, axis=0):
    """ Return the minimum and maximum coordinates along axis

    parameter:
    ----------
        axis:
            axis

    returns:
    -------
        tuple: minV, maxV

    """
    maxVal = np.zeros((1))
    minVal = np.zeros((1))
    maxVal[0] = mesh.data[:, axis].max()
    minVal[0] = mesh.data[:, axis].min()

    uw.barrier()
    comm.Allreduce(MPI.IN_PLACE, maxVal, op=MPI.MAX)
    comm.Allreduce(MPI.IN_PLACE, minVal, op=MPI.MIN)
    uw.barrier()

    return minVal, maxVal


class Plots(object):

    def __init__(self, Model):

        self.Model = Model

    @property
    def _boundingBox(self):
        minCoord = tuple([nd(val) for val in self.Model.minCoord])
        maxCoord = tuple([nd(val) for val in self.Model.maxCoord])
        boundingBox = (minCoord, maxCoord)
        return boundingBox

    def materialField(self, figsize=None, title="Material Field",
                      colours=None, script=None, cullface=False,
                      mask=None, visugrid=None, onMesh=False,
                      show=True, store=None, quality=3,
                      **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title
        Fig["boundingBox"] = self._boundingBox

        if onMesh:
            Fig.Surface(self.Model.mesh, self.Model.projMaterialField,
                        **kwargs)
        else:
            pts = Fig.Points(self.Model.swarm,
                             fn_colour=self.Model.materialField,
                             colours=colours,
                             cullface=cullface, name=Fig["title"], **kwargs)
            # pts.colourBar["binlabels"] = True
            # pts.colourBar["align"] = "right"
            # pts.colourBar["vertical"] = True
            pts.colourBar.colourMap["discrete"] = True

        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            # Fig.viewer().window()
            Fig.show()

        return Fig

    material = materialField

    def viscosityField(self, figsize=None, title="Viscosity Field",
                       units=u.pascal * u.second, logScale=True,
                       projected=False, cullface=False,
                       script=None, show=True, quality=3,
                       store=None, visugrid=None, **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title + " " + str(units)
        Fig["boundingBox"] = self._boundingBox

        fact = Dimensionalize(1.0, units).magnitude
        Fig.Points(self.Model.swarm, self.Model._viscosityFn * fact,
                   logScale=logScale, name=Fig["title"], cullface=cullface, **kwargs)

        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    viscosity = viscosityField

    def strainRate(self, figsize=None, title="Strain Rate Field",
                   units=1.0 / u.second,
                   cullface=False,
                   logScale=True, colours="coolwarm",
                   script=None, show=True, quality=3,
                   store=None, visugrid=None, **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title + " " + str(units)
        Fig["boundingBox"] = self._boundingBox

        fact = Dimensionalize(1.0, units).magnitude
        Fig.Surface(self.Model.mesh.subMesh,
                    self.Model.strainRateField * fact,
                    cullface=cullface, logScale=logScale, name=Fig["title"],
                    colours=colours,
                    **kwargs)

        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    def density(self, figsize=None, title="Density Field",
                units=u.kilogram / u.metre**3, quality=3,
                script=None, cullface=False, show=True,
                store=None, visugrid=None, **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title + " " + str(units)
        Fig["boundingBox"] = self._boundingBox

        fact = Dimensionalize(1.0, units).magnitude
        Fig.Points(self.Model.swarm,
                   fn_colour=self.Model._densityFn * fact,
                   cullface=cullface, name=Fig["title"], **kwargs)

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    def temperature(self, figsize=None, title="Temperature Field",
                    units=u.degK, script=None, cullface=False,
                    colours="coolwarm", show=True, quality=3,
                    store=None, visugrid=None, **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title + " " + str(units)
        Fig["boundingBox"] = self._boundingBox

        fact = Dimensionalize(1.0, units).magnitude
        Fig.Surface(self.Model.mesh, self.Model.temperature * fact,
                    colours=colours, cullface=cullface, name=Fig["title"],
                    **kwargs)
        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    def pressureField(self, figsize=None, title="Pressure Field",
                      units=u.pascal, cullface=False,
                      script=None, show=True, quality=3,
                      store=None, visugrid=None, **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title + " " + str(units)
        Fig["boundingBox"] = self._boundingBox

        fact = Dimensionalize(1.0, units).magnitude
        Fig.Surface(self.Model.mesh, self.Model.pressureField * fact,
                    cullface=cullface, name=Fig["title"], **kwargs)
        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    def stressField(self, figsize=None, title="Stress Field",
                    units=u.pascal, cullface=False,
                    script=None, show=True, quality=3,
                    store=None, visugrid=None, **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title + " " + str(units)
        Fig["boundingBox"] = self._boundingBox

        fact = Dimensionalize(1.0, units).magnitude
        Fig.Surface(self.Model.mesh, self.Model.projStressField * fact,
                    cullface=cullface, name=Fig["title"], **kwargs)
        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    def velocityField(self, figsize=None, title="Velocity Field",
                      units=u.centimeter / u.year, cullface=False,
                      script=None, show=True, quality=3,
                      store=None, colours='diverge', visugrid=None,
                      arrowlength=0.0,
                      arrownorm=1.0,
                      arrowres=(16,16,16), **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title + " " + str(units)
        Fig["boundingBox"] = self._boundingBox

        fact = Dimensionalize(1.0, units).magnitude
        velmagfield = uw.function.math.sqrt(
            uw.function.math.dot(self.Model.velocityField,
                                 self.Model.velocityField))
        Fig.Surface(self.Model.mesh, velmagfield * fact,colours=colours,
                   cullface=cullface, name=Fig["title"], **kwargs)
        Fig.VectorArrows(self.Model.mesh,
                         self.Model.velocityField,
                         length=arrowlength,
                         normalise=arrownorm,
                         resolution=arrowres,
                         **kwargs)
        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    def plasticStrain(self, figsize=None, title="Plastic Strain",
                      cullface=False, script=None, show=True,
                      store=None, visugrid=None, quality=3,
                      **kwargs):

        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title
        Fig["boundingBox"] = self._boundingBox

        Fig.Points(self.Model.swarm, fn_colour=self.Model.plasticStrain,
                   cullface=cullface, name=Fig["title"], **kwargs)
        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)
        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    plastic_strain = plasticStrain

    def melt_fraction(self, figsize=None, title="Melt fraction",
                      cullface=False, script=None, show=True,
                      store=None, visugrid=None, quality=3,
                      **kwargs):

        self.Model.update_melt_fraction()
        Fig = glucifer.Figure(store=store, figsize=figsize,
                              quality=quality,
                              min=self._boundingBox[0],
                              max=self._boundingBox[1])
        Fig["title"] = title
        Fig["boundingBox"] = self._boundingBox

        Fig.Points(self.Model.swarm, fn_colour=self.Model.meltField,
                   cullface=cullface, name=Fig["title"], **kwargs)

        if visugrid:
            clip_X, clip_Y = _visugrid_drawing_object(self.Model, visugrid)
            Fig.Mesh(visugrid.mesh, xmin=clip_X[0], xmax=clip_X[1],
                     ymin=clip_Y[0], ymax=clip_Y[1])

        Fig.script(script)

        if show and glucifer.lavavu.is_notebook():
            Fig.show()

        return Fig

    def profile(self,
                start_point,
                end_point,
                field,
                field_units=u.dimensionless,
                distance_units=u.dimensionless,
                npoints=1000):

        if (field not in rcParams["mesh.variables"] and
           field not in rcParams["swarm.variables"]):
            raise ValueError("""{0} is not a valid field, \n
                                Valid fields are {1} or {2}""".format(
                             field, rcParams["mesh.variables"],
                             rcParams["swarm.variables"]))

        start_point = np.array([nd(val) for val in start_point])
        end_point = np.array([nd(val) for val in end_point])

        points = [start_point, end_point]
        x_coords, y_coords = zip(*points)

        x = np.linspace(x_coords[0], x_coords[1], npoints)

        if x_coords[0] == x_coords[1]:
            y = np.linspace(y_coords[0], y_coords[1], npoints)
        else:
            f = interpolate.interp1d(x_coords, y_coords)
            y = f(x)

        dx = np.diff(x)
        dy = np.diff(y)
        distances = np.zeros(x.shape)
        distances[1:] = np.sqrt(dx**2 + dy**2)
        distances = np.cumsum(distances)

        obj = getattr(self.Model, field)

        if isinstance(obj, SwarmVariable):
            obj = getattr(self.Model, "proj" + field[0].upper() + field[1:])

        pts = np.array(zip(x, y))

        values = obj.evaluate(pts)

        distance_fact = Dimensionalize(1.0, distance_units)
        field_fact = Dimensionalize(1.0, field_units)

        distances *= distance_fact.magnitude
        values *= field_fact.magnitude

        return distances, values

    def christmas(self, position):
        return self.profile(start_point=[position, self.Model.top],
                            end_point=[position, self.Model.bottom],
                            field="viscosityField")


