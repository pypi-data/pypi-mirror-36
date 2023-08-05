# -*- coding: utf-8 -*-
"""This module contains different types of finite element meshes.

Meshes are created using various built-in constructors or loaded from external
formats using `meshio <https://github.com/nschloe/meshio>`_. See the following
implementations:

- :class:`~skfem.mesh.MeshTri`, triangular mesh
- :class:`~skfem.mesh.MeshQuad`, quadrilateral mesh
- :class:`~skfem.mesh.MeshTet`, tetrahedral mesh
- :class:`~skfem.mesh.MeshHex`, hexahedral mesh
- :class:`~skfem.mesh.MeshLine`, one-dimensional mesh

"""

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import warnings
from scipy.sparse import coo_matrix

import skfem.mapping
import skfem.element

from typing import Optional, Union, Tuple,\
                   Any, NamedTuple, Type,\
                   TypeVar, Dict, Callable
from numpy import ndarray
from matplotlib.axes import Axes

MeshType = TypeVar('MeshType', bound='Mesh')
DimTuple = Union[Tuple[float], Tuple[float, float], Tuple[float, float, float]]


class Submesh(NamedTuple):
    """Index arrays that define subsets of mesh topological entities."""
    p: Optional[ndarray] = None
    t: Optional[ndarray] = None
    facets: Optional[ndarray] = None
    edges: Optional[ndarray] = None


class Mesh():
    """A finite element mesh.
    
    This is an abstract superclass. See the following implementations:

    - :class:`~skfem.mesh.MeshTri`, triangular mesh
    - :class:`~skfem.mesh.MeshTet`, tetrahedral mesh
    - :class:`~skfem.mesh.MeshQuad`, quadrilateral mesh
    - :class:`~skfem.mesh.MeshHex`, hexahedral mesh
    - :class:`~skfem.mesh.MeshLine`, one-dimensional mesh

    """

    refdom: str = "none"  
    brefdom: str = "none" 
    meshio_type: str = "none"

    p: ndarray = np.array([]) 
    t: ndarray = np.array([]) 

    def __init__(self):
        """Check that p and t are C_CONTIGUOUS as this leads
        to better performance."""
        if self.p is not None:
            if self.p.flags['F_CONTIGUOUS']:
                if self.p.shape[1]>1000:
                    warnings.warn("Mesh.__init__(): Transforming " +
                            "over 100 vertices to C_CONTIGUOUS.")
                self.p = np.ascontiguousarray(self.p)
        if self.t is not None:
            if self.t.flags['F_CONTIGUOUS']:
                if self.t.shape[1]>1000:
                    warnings.warn("Mesh.__init__(): Transforming " +
                            "over 100 elements to C_CONTIGUOUS.")
                self.t = np.ascontiguousarray(self.t)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Mesh of type '" + str(type(self)) + "' "\
               "with " + str(self.p.shape) + " vertices " \
               "and " + str(self.t.shape) + " elements."

    def show(self):
        """A wrapper for matplotlib.pyplot.show()."""
        plt.show()

    def dim(self):
        """Return the spatial dimension of the mesh."""
        return int(self.p.shape[0])

    def mapping(self):
        """Default local-to-global mapping for the mesh."""
        raise NotImplementedError("Default mapping not implemented!")

    def _uniform_refine(self):
        """Perform a single uniform mesh refinement."""
        raise NotImplementedError("Single refine not implemented " +
                                  "for this mesh type!")

    def refine(self, no_refs: Optional[int] = None):
        """Refine the mesh.
        
        Parameters
        ----------
        no_refs
            Perform multiple refinements.

        """
        if no_refs is None:
            return self._uniform_refine()
        else:
            for itr in range(no_refs):
                self._uniform_refine()

    def remove_elements(self, element_indices: ndarray) -> MeshType:
        """Construct new mesh with elements removed
        based on their indices.

        Parameters
        ----------
        element_indices
            List of element indices to remove.

        Returns
        -------
        Mesh
            A new mesh object with the requested elements removed.

        """
        keep = np.setdiff1d(np.arange(self.t.shape[1]), element_indices)
        newt = self.t[:, keep]
        ptix = np.unique(newt)
        reverse = np.zeros(self.p.shape[1])
        reverse[ptix] = np.arange(len(ptix))
        newt = reverse[newt]
        newp = self.p[:, ptix]
        meshclass = type(self)
        return meshclass(newp, newt.astype(np.intp))

    def scale(self, scale: Union[float, DimTuple]) -> None:
        """Scale the mesh.

        Parameters
        ----------
        scale
            Scale each dimension by this factor. If a single float is provided,
            same scaling is used for all dimensions. Otherwise, provide a
            tuple which has same size as the mesh dimension.

        """
        for itr in range(int(self.dim())):
            if isinstance(scale, tuple):
                self.p[itr, :] *= scale[itr]
            else:
                self.p[itr, :] *= scale

    def translate(self, vec: DimTuple) -> None:
        """Translate the mesh.

        Parameters
        ----------
        vec
            Translate the mesh by a vector. Must have same size as the mesh
            dimension.

        """
        for itr in range(int(self.dim())):
            self.p[itr, :] += vec[itr]

    def _validate(self):
        """Perform mesh validity checks."""
        # check that element connectivity contains integers
        # NOTE: this is neccessary for some plotting functionality
        if not np.issubdtype(self.t[0, 0], np.signedinteger):
            msg = ("Mesh._validate(): Element connectivity "
                   "must consist of integers.")
            raise Exception(msg)
        # check that vertex matrix has "correct" size
        if self.p.shape[0] > 3:
            msg = ("Mesh._validate(): We do not allow meshes "
                   "embedded into larger than 3-dimensional "
                   "Euclidean space! Please check that "
                   "the given vertex matrix is of size Ndim x Nvertices.")
            raise Exception(msg)
        # check that element connectivity matrix has correct size
        nvertices = {'line': 2, 'tri': 3, 'quad': 4, 'tet': 4, 'hex': 8}
        if self.t.shape[0] != nvertices[self.refdom]:
            msg = ("Mesh._validate(): The given connectivity "
                   "matrix has wrong shape!")
            raise Exception(msg)
        # check that there are no duplicate points
        tmp = np.ascontiguousarray(self.p.T)
        if self.p.shape[1] != np.unique(tmp.view([('', tmp.dtype)]
                                                 * tmp.shape[1])).shape[0]:
            msg = "Mesh._validate(): Mesh contains duplicate vertices."
            warnings.warn(msg)
        # check that all points are at least in some element
        if len(np.setdiff1d(np.arange(self.p.shape[1]), np.unique(self.t))):
            msg = ("Mesh._validate(): Mesh contains a vertex "
                   "not belonging to any element.")
            raise Exception(msg)

    def save(self,
             filename: str,
             pointData: Optional[Union[ndarray, Dict[str, ndarray]]] = None,
             cellData: Optional[Union[ndarray, Dict[str, ndarray]]] = None) -> None:
        """Export the mesh and fields using meshio.

        Parameters
        ----------
        filename
            The filename for vtk-file.
        pointData
            Data related to the vertices of the mesh. Numpy array for one
            output or dict for multiple.
        cellData
            Data related to the elements of the mesh. Numpy array for one
            output or dict for multiple

        """
        import meshio

        if pointData is not None:
            if type(pointData) != dict:
                pointData = {'0':pointData}

        if cellData is not None:
            if type(cellData) != dict:
                cellData = {'0':cellData}

        cells = { self.meshio_type : self.t.T }
        mesh = meshio.Mesh(self.p.T, cells, pointData, cellData)
        meshio.write(filename, mesh)

    @classmethod
    def load(cls: Type[MeshType], filename: str) -> MeshType:
        """Load an external mesh from file using `meshio
        <https://github.com/nschloe/meshio>`_.
        
        Parameters
        ----------
        filename
            The filename of the mesh.

        """
        import meshio
        meshdata = meshio.read(filename)
        if cls.meshio_type in meshdata.cells:
            if issubclass(cls, Mesh2D):
                p = meshdata.points[:, :2].T
            else:
                p = meshdata.points.T
            t = meshdata.cells[cls.meshio_type].T
            mesh = cls(p, t)
            # load submeshes, currently gmsh only
            try:
                bnd_type = {
                        'triangle':'line',
                        'quad':'line',
                        'tetra':'triangle',
                        'hexahedron':'quad',
                        }[cls.meshio_type]
                if bnd_type in meshdata.cells:
                    facets = meshdata.cells[bnd_type]
                    facets_tag = meshdata.cell_data[bnd_type]['gmsh:physical']
                    bndfacets = mesh.boundary_facets()
                    # put Mesh.facets to dict
                    dic = {tuple(np.sort(facets[i])): facets_tag[i] for i in range(facets.shape[0])}
                    # get index of corresponding Mesh.facets for each meshio
                    # facet is found in the dict
                    ix = np.array([[dic[tuple(np.sort(mesh.facets[:, i]))], i]
                                     for i in bndfacets
                                     if tuple(np.sort(mesh.facets[:, i])) in dic])
                    # read meshio tag numbers and names
                    tags = ix[:, 0]
                    facet_ix = {}
                    def find_tagname(t):
                        for key in meshdata.field_data:
                            if meshdata.field_data[key][0] == t:
                                return key
                    for tag in np.unique(tags):
                        tagix = np.nonzero(tags == tag)[0]
                        facet_ix[find_tagname(tag)] = ix[tagix, 1]
                    nodes_ix = {key: np.unique(mesh.facets[:, facet_ix[key]].flatten())
                                     for key in facet_ix}
                    # save submesh info to mesh.boundaries
                    mesh.boundaries = {key: Submesh(p = nodes_ix[key], facets = facet_ix[key])
                                      for key in facet_ix}
                    # TODO edges
            except Exception:
                # all mesh formats are not supported; raise warning for
                # unsupported types
                warnings.warn("Could not load submeshes.")
            return mesh
        else:
            raise Exception("The mesh contains no elements of type "
                            + cls.meshio_type)


class Mesh3D(Mesh):
    """Three dimensional meshes, common methods.

    See the following implementations:

    - :class:`~skfem.mesh.MeshTet`, tetrahedral mesh
    - :class:`~skfem.mesh.MeshHex`, hexahedral mesh

    """

    def nodes_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return nodes that satisfy some condition.

        Parameters
        ----------
        test
            Evaluates to 1 or True for nodes belonging to the output set.

        """
        return np.nonzero(test(self.p[0, :], self.p[1, :], self.p[2, :]))[0]

    def facets_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return facets whose midpoints satisfy some condition.
        
        Parameters
        ----------
        test
            Evaluates to 1 or True for facet midpoints of the facets belonging
            to the output set.

        """
        mx = np.sum(self.p[0, self.facets], axis=0)/self.facets.shape[0]
        my = np.sum(self.p[1, self.facets], axis=0)/self.facets.shape[0]
        mz = np.sum(self.p[2, self.facets], axis=0)/self.facets.shape[0]
        return np.nonzero(test(mx, my, mz))[0]

    def edges_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return edges whose midpoints satisfy some condition.

        Parameters
        ----------
        test
            Evaluates to 1 or True for edge midpoints of the edges belonging to
            the output set.

        """
        mx = 0.5*(self.p[0, self.edges[0, :]] + self.p[0, self.edges[1, :]])
        my = 0.5*(self.p[1, self.edges[0, :]] + self.p[1, self.edges[1, :]])
        mz = 0.5*(self.p[2, self.edges[0, :]] + self.p[2, self.edges[1, :]])
        return np.nonzero(test(mx, my, mz))[0]

    def elements_satisfying(self, test: Callable[[float, float, float], bool]) -> ndarray:
        """Return elements whose midpoints satisfy some condition.

        Parameters
        ----------
        test
            Evaluates to 1 or True for element midpoints of the elements
            belonging to the output set.

        """
        mx = np.sum(self.p[0, self.t], axis=0)/self.t.shape[0]
        my = np.sum(self.p[1, self.t], axis=0)/self.t.shape[0]
        mz = np.sum(self.p[2, self.t], axis=0)/self.t.shape[0]
        return np.nonzero(test(mx, my, mz))[0]

    def submesh(self, test: Callable[[float, float, float], bool]) -> Submesh:
        """Return Submesh object where all topological entities satisfy some
        condition.
        
        Parameters
        ----------
        test
            Evaluates to 1 or True for the midpoints of the topological
            entities belonging to the output Submesh.

        """
        p = self.nodes_satisfying(test)
        if len(p) == 0:
            p = None
        facets = self.facets_satisfying(test)
        if len(facets) == 0:
            facets = None
        edges = self.edges_satisfying(test)
        if len(edges) == 0:
            edges = None
        t = self.elements_satisfying(test)
        if len(t) == 0:
            t = None
        return Submesh(p=p, facets=facets, edges=edges, t=t)

    def boundary_nodes(self) -> ndarray:
        """Return an array of boundary node indices."""
        return np.unique(self.facets[:, self.boundary_facets()])

    def boundary_facets(self) -> ndarray:
        """Return an array of boundary facet indices."""
        return np.nonzero(self.f2t[1, :] == -1)[0]

    def interior_facets(self) -> ndarray:
        """Return an array of interior facet indices."""
        return np.nonzero(self.f2t[1, :] >= 0)[0]

    def boundary_edges(self) -> ndarray:
        """Return an array of boundary edge indices."""
        bnodes = self.boundary_nodes()[:, None]
        return np.nonzero(np.sum(self.edges[0, :] == bnodes, axis=0) *
                          np.sum(self.edges[1, :] == bnodes, axis=0))[0]

    def interior_nodes(self) -> ndarray:
        """Return an array of interior node indices."""
        return np.setdiff1d(np.arange(0, self.p.shape[1]), self.boundary_nodes())

    def param(self) -> float:
        """Return (maximum) mesh parameter."""
        return np.max(np.sqrt(np.sum((self.p[:, self.edges[0, :]] -
                                      self.p[:, self.edges[1, :]])**2, axis=0)))


class Mesh2D(Mesh):
    """Two dimensional meshes, common methods.
    
    See the following implementations:

    - :class:`~skfem.mesh.MeshTri`, triangular mesh
    - :class:`~skfem.mesh.MeshQuad`, quadrilateral mesh

    """

    def boundary_nodes(self) -> ndarray:
        """Return an array of boundary node indices."""
        return np.unique(self.facets[:, self.boundary_facets()])

    def interior_nodes(self) -> ndarray:
        """Return an array of interior node indices."""
        return np.setdiff1d(np.arange(0, self.p.shape[1]), self.boundary_nodes())

    def nodes_satisfying(self, test: Callable[[float, float], bool]) -> ndarray:
        """Return nodes that satisfy some condition.

        Parameters
        ----------
        test
            A function which returns True for the set of nodes that are to be
            included in the return set.

        """
        return np.nonzero(test(self.p[0, :], self.p[1, :]))[0]

    def facets_satisfying(self, test: Callable[[float, float], bool]) -> ndarray:
        """Return facets whose midpoints satisfy some condition.

        Parameters
        ----------
        test
            A function which returns True for the facet midpoints that are to
            be included in the return set.

        """
        mx = 0.5*(self.p[0, self.facets[0, :]] + self.p[0, self.facets[1, :]])
        my = 0.5*(self.p[1, self.facets[0, :]] + self.p[1, self.facets[1, :]])
        return np.nonzero(test(mx, my))[0]

    def elements_satisfying(self, test: Callable[[float, float], bool]) -> ndarray:
        """Return elements whose midpoints satisfy some condition.

        Parameters
        ----------
        test
            A function which returns True for the element midpoints that are to
            be included in the return set.

        """
        mx = np.sum(self.p[0, self.t], axis=0)/self.t.shape[0]
        my = np.sum(self.p[1, self.t], axis=0)/self.t.shape[0]
        return np.nonzero(test(mx, my))[0]
    
    def submesh(self, test: Callable[[float, float], bool]) -> Submesh:
        """Return Submesh object where all topological entities satisfy some
        condition.
        
        Parameters
        ----------
        test
            Evaluates to 1 or True for the midpoints of the topological
            entities belonging to the output Submesh.

        """
        p = self.nodes_satisfying(test)
        if len(p) == 0:
            p = None
        facets = self.facets_satisfying(test)
        if len(facets) == 0:
            facets = None
        t = self.elements_satisfying(test)
        if len(t) == 0:
            t = None
        return Submesh(p=p, facets=facets, edges=None, t=t)

    def interior_facets(self) -> ndarray:
        """Return an array of interior facet indices."""
        return np.nonzero(self.f2t[1, :] >= 0)[0]

    def boundary_facets(self) -> ndarray:
        """Return an array of boundary facet indices."""
        return np.nonzero(self.f2t[1, :] == -1)[0]

    def draw(self,
             ax: Optional[Axes] = None,
             node_numbering: Optional[bool] = False,
             facet_numbering: Optional[bool] = False,
             element_numbering: Optional[bool] = False,
             aspect: float = 1.) -> Axes:
        """Visualise a mesh by drawing the edges.

        Parameters
        ----------
        ax
            A preinitialised Matplotlib axes for plotting.
        node_numbering
            If true, draw node numbering.
        facet_numbering
            If true, draw facet numbering.
        element_numbering
            If true, draw element numbering.
        aspect
            Ratio of vertical to horizontal length-scales; ignored if ax
            specified

        Returns
        -------
        Axes
            The Matplotlib axes onto which the mesh was plotted.

        """
        if ax is None:
            # create new figure
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_aspect(aspect)
        # visualize the mesh faster plotting is achieved through
        # None insertion trick.
        xs = []
        ys = []
        for s, t, u, v in zip(self.p[0, self.facets[0, :]],
                              self.p[1, self.facets[0, :]],
                              self.p[0, self.facets[1, :]],
                              self.p[1, self.facets[1, :]]):
            xs.append(s)
            xs.append(u)
            xs.append(None)
            ys.append(t)
            ys.append(v)
            ys.append(None)
        ax.plot(xs, ys, 'k', linewidth='0.5')

        if node_numbering:
            for itr in range(self.p.shape[1]):
                ax.text(self.p[0, itr], self.p[1, itr], str(itr))

        if facet_numbering:
            mx = .5*(self.p[0, self.facets[0, :]] + self.p[0, self.facets[1, :]])
            my = .5*(self.p[1, self.facets[0, :]] + self.p[1, self.facets[1, :]])
            for itr in range(self.facets.shape[1]):
                ax.text(mx[itr], my[itr], str(itr))

        if element_numbering:
            mx = np.sum(self.p[0, self.t], axis=0)/self.t.shape[0]
            my = np.sum(self.p[1, self.t], axis=0)/self.t.shape[0]
            for itr in range(self.t.shape[1]):
                ax.text(mx[itr], my[itr], str(itr))

        return ax

    def mirror_mesh(self, a: float, b: float, c: float) -> MeshType:
        """Mirror a mesh by the line :math:`ax + by + c = 0`."""
        tmp = -2.0*(a*self.p[0, :] + b*self.p[1, :] + c)/(a**2 + b**2)
        newx = a*tmp + self.p[0, :]
        newy = b*tmp + self.p[1, :]
        newpoints = np.vstack((newx, newy))
        points = np.hstack((self.p, newpoints))
        tris = np.hstack((self.t, self.t + self.p.shape[1]))

        # remove duplicates
        tmp = np.ascontiguousarray(points.T)
        tmp, ixa, ixb = np.unique(tmp.view([('', tmp.dtype)]*tmp.shape[1]), return_index=True, return_inverse=True)
        points = points[:, ixa]
        tris = ixb[tris]

        meshclass = type(self)

        return meshclass(points, tris)

    def save(self,
            filename: str,
            pointData: Optional[Union[ndarray, Dict[str, ndarray]]] = None,
            cellData: Optional[Union[ndarray, Dict[str, ndarray]]] = None) -> None:
        """Export the mesh and fields using meshio. (2D version.)

        Parameters
        ----------
        filename
            The filename for vtk-file.
        pointData
            Data related to the vertices of the mesh. Numpy array for one
            output or dict for multiple.
        cellData
            Data related to the elements of the mesh. Numpy array for one
            output or dict for multiple

        """
        import meshio

        # a row of zeros required in 2D
        p = np.vstack((np.zeros(self.p.shape[1]), self.p))

        if pointData is not None:
            if type(pointData) != dict:
                pointData = {'0':pointData}

        if cellData is not None:
            if type(cellData) != dict:
                cellData = {'0':cellData}

        cells = { self.meshio_type : self.t.T }
        mesh = meshio.Mesh(p.T, cells, pointData, cellData)
        meshio.write(filename, mesh)

    def param(self) -> float:
        """Return mesh parameter."""
        return np.max(np.sqrt(np.sum((self.p[:, self.facets[0, :]] -
                                      self.p[:, self.facets[1, :]])**2, axis=0)))


class InterfaceMesh1D(Mesh):
    """An interface mesh for mortar methods."""
    def __init__(self, mesh1, mesh2, rule, param, debug_plot=False):
        self.brefdom = mesh1.brefdom

        p1_ix = mesh1.nodes_satisfying(rule)
        p2_ix = mesh2.nodes_satisfying(rule)

        p1 = mesh1.p[:, p1_ix]
        p2 = mesh2.p[:, p2_ix]
        _, ix = np.unique(np.concatenate((param(p1[0, :], p1[1, :]), param(p2[0, :], p2[1, :]))), return_index=True)

        np1 = mesh1.p.shape[1]
        nt1 = mesh1.t.shape[1]
        ixorig = np.concatenate((p1_ix, p2_ix + np1))[ix]

        self.p = np.hstack((mesh1.p, mesh2.p))
        self.t = np.hstack((mesh1.t, mesh2.t + np1))
        self.facets = np.array([ixorig[:-1], ixorig[1:]])
        self.t2f = -1 + 0*np.hstack((mesh1.t2f, mesh2.t2f))

        # construct normals
        tangent_x = self.p[0, self.facets[0, :]] - self.p[0, self.facets[1, :]]
        tangent_y = self.p[1, self.facets[0, :]] - self.p[1, self.facets[1, :]]
        tangent_lengths = np.sqrt(tangent_x**2 + tangent_y**2)

        self.normals = np.array([-tangent_y/tangent_lengths, tangent_x/tangent_lengths])

        if debug_plot:
            ax = mesh1.draw()
            mesh2.draw(ax=ax)
            xs = np.array([self.p[0, self.facets[0, :]], self.p[0, self.facets[1, :]]])
            midx = np.sum(xs, axis=0)/2.0
            ys = np.array([self.p[1, self.facets[0, :]], self.p[1, self.facets[1, :]]])
            midy = np.sum(ys, axis=0)/2.0
            xs = 0.9*(xs - midx) + midx
            ys = 0.9*(ys - midy) + midy
            ax.plot(xs, ys, 'x-')

        # mappings from facets to the original triangles
        # TODO vectorize
        self.f2t = self.facets*0-1
        for itr in range(self.facets.shape[1]):
            mx = .5*(self.p[0, self.facets[0, itr]] + self.p[0, self.facets[1, itr]])
            my = .5*(self.p[1, self.facets[0, itr]] + self.p[1, self.facets[1, itr]])
            val = param(mx, my)
            for jtr in mesh1.boundary_facets():
                fix1 = mesh1.facets[0, jtr]
                x1 = mesh1.p[0, fix1]
                y1 = mesh1.p[1, fix1]
                fix2 = mesh1.facets[1, jtr]
                x2 = mesh1.p[0, fix2]
                y2 = mesh1.p[1, fix2]
                if rule(x1, y1) > 0 or rule(x2, y2) > 0:
                    if val > param(x1, y1) and val < param(x2, y2):
                        # OK
                        self.f2t[0, itr] = mesh1.f2t[0, jtr]
                        break
                    elif val < param(x1, y1) and val > param(x2, y2): # ye olde
                        # OK
                        self.f2t[0, itr] = mesh1.f2t[0, jtr]
                        break
                    elif val >= param(x1, y1) and val < param(x2, y2):
                        # OK
                        self.f2t[0, itr] = mesh1.f2t[0, jtr]
                        break
                    elif val > param(x1, y1) and val <= param(x2, y2):
                        # OK
                        self.f2t[0, itr] = mesh1.f2t[0, jtr]
                        break
                    elif val <= param(x1, y1) and val > param(x2, y2):
                        # OK
                        self.f2t[0, itr] = mesh1.f2t[0, jtr]
                        break
                    elif val < param(x1, y1) and val >= param(x2, y2):
                        # OK
                        self.f2t[0, itr] = mesh1.f2t[0, jtr]
                        break
            for jtr in mesh2.boundary_facets():
                fix1 = mesh2.facets[0, jtr]
                x1 = mesh2.p[0, fix1]
                y1 = mesh2.p[1, fix1]
                fix2 = mesh2.facets[1, jtr]
                x2 = mesh2.p[0, fix2]
                y2 = mesh2.p[1, fix2]
                if rule(x1, y1) > 0 or rule(x2, y2) > 0:
                    if val > param(x1, y1) and val < param(x2, y2):
                        # OK
                        self.f2t[1, itr] = mesh2.f2t[0, jtr] + nt1
                        break
                    elif val < param(x1, y1) and val > param(x2, y2):
                        # OK
                        self.f2t[1, itr] = mesh2.f2t[0, jtr] + nt1
                        break
                    elif val >= param(x1, y1) and val < param(x2, y2):
                        # OK
                        self.f2t[1, itr] = mesh2.f2t[0, jtr] + nt1
                        break
                    elif val > param(x1, y1) and val <= param(x2, y2):
                        # OK
                        self.f2t[1, itr] = mesh2.f2t[0, jtr] + nt1
                        break
                    elif val <= param(x1, y1) and val > param(x2, y2):
                        # OK
                        self.f2t[1, itr] = mesh2.f2t[0, jtr] + nt1
                        break
                    elif val < param(x1, y1) and val >= param(x2, y2):
                        # OK
                        self.f2t[1, itr] = mesh2.f2t[0, jtr] + nt1
                        break
        if (self.f2t>-1).all():
            self.f2t[0, :]
            return
        else:
            print(self.f2t)
            raise Exception("All mesh facets corresponding to mortar facets not found!")


class MeshLine(Mesh):
    """One-dimensional mesh."""

    refdom = "line"
    brefdom = "point"

    p = np.array([])
    t = np.array([])

    def __init__(self, p=None, t=None, validate=True):
        if p is None and t is None:
            p = np.array([[0, 1]])
        if len(p.shape)==1:
            p = np.array([p]) 
        self.p = p
        self._build_mappings()

        if validate:
            self._validate()
        super(MeshLine, self).__init__()

    @classmethod
    def init_refdom(cls: Type[MeshType]) -> MeshType:
        """Initialise a mesh constisting of the reference interval [0,1]."""
        return cls()

    def _build_mappings(self):
        """Build t2f and f2t. Also sorts p and builds t."""
        self.p = np.sort(self.p)
        self.t = np.array([np.arange(np.max(self.p.shape)-1), np.arange(np.max(self.p.shape)-1)+1])

        self.facets = np.array([np.arange(self.p.shape[1])])
        self.t2f = self.t
        # build f2t
        e_tmp = np.hstack((self.t2f[0, :], self.t2f[1, :]))
        t_tmp = np.tile(np.arange(self.t.shape[1]), (1, 2))[0]

        e_first, ix_first = np.unique(e_tmp, return_index=True)
        e_last, ix_last = np.unique(e_tmp[::-1], return_index=True)
        ix_last = e_tmp.shape[0] - ix_last - 1

        self.f2t = np.zeros((2, self.facets.shape[1]), dtype=np.int64)
        self.f2t[0, e_first] = t_tmp[ix_first]
        self.f2t[1, e_last] = t_tmp[ix_last]

        # second row to zero if repeated (i.e., on boundary)
        self.f2t[1, np.nonzero(self.f2t[0, :] == self.f2t[1, :])[0]] = -1

    def adaptive_refine(self, marked):
        """Perform an adaptive refine which splits each marked element into two."""
        t = self.t
        p = self.p

        mid = range(len(marked)) + np.max(t) + 1

        nonmarked = np.setdiff1d(np.arange(t.shape[1]), marked)

        newp = np.hstack((p, 0.5*(p[:, self.t[0, marked]] + p[:, self.t[1, marked]])))
        newt = np.vstack((t[0, marked], mid))
        newt = np.hstack((t[:, nonmarked], newt, np.vstack((mid, t[1, marked]))))
        # update fields
        self.p = newp
        self.t = newt

    def nodes_satisfying(self, test):
        """Return nodes that satisfy some condition.

        Parameters
        ----------
        test : lambda function (1 param)
            Evaluates to 1 or True for nodes belonging
            to the output set.

        """
        return np.nonzero(test(self.p[0, :]))[0]

    def _uniform_refine(self):
        """Perform a single mesh refine that halves 'h'."""
        # rename variables
        p = self.p

        mid = range(self.t.shape[1]) + np.max(self.t) + 1
        # new vertices and elements
        newp = np.hstack((p, 0.5*(p[:, self.t[0, :]] + p[:, self.t[1, :]])))
        # update fields
        self.p = newp
        self._build_mappings()

        # TODO implement prolongation

    def boundary_nodes(self):
        """Find the boundary nodes of the mesh."""
        _, counts = np.unique(self.t.flatten(), return_counts=True)
        return np.nonzero(counts == 1)[0]

    def interior_nodes(self):
        """Find the interior nodes of the mesh."""
        _, counts = np.unique(self.t.flatten(), return_counts=True)
        return np.nonzero(counts == 2)[0]

    def plot(self, u, ax=None, color='ko-'):
        """Plot a function defined at the nodes of the mesh."""
        if ax is None:
            # create new figure
            fig = plt.figure()
            ax = fig.add_subplot(111)
        xs = []
        ys = []
        for y1, y2, s, t in zip(u[self.t[0, :]],
                                u[self.t[1, :]],
                                self.p[0, self.t[0, :]],
                                self.p[0, self.t[1, :]]):
            xs.append(s)
            xs.append(t)
            xs.append(None)
            ys.append(y1)
            ys.append(y2)
            ys.append(None)
        ax.plot(xs, ys, color)

        return ax

    def __mul__(self, other):
        """Tensor product mesh."""
        return MeshQuad.init_tensor(self.p[0, :], other.p[0, :])

    def param(self):
        return np.max(np.abs(self.p[0, self.t[1, :]] - self.p[0, self.t[0, :]]))

    def mapping(self):
        return skfem.mapping.MappingAffine(self)


class MeshQuad(Mesh2D):
    """A mesh consisting of quadrilateral elements.
    
    Attributes
    ----------
    p
        An array containing the vertices of the mesh (2 x Nvertices).
    t
        An array containing the element connectivity (4 x Nelemens).
    facets
        Each column contains a pair of indices to p (2 x Nfacets).
    f2t
        Each column contains a pair of indices to t or -1 on the
        second row if the facet is on the boundary (2 x Nfacets).
    t2f
        Each column contains four indices to facets (4 x Nelements).
    
    Examples
    --------
    Initialise a tensor-product mesh.
    
    >>> from skfem.mesh import MeshQuad
    >>> import numpy as np
    >>> m = MeshQuad.init_tensor(np.linspace(0, 1, 10), np.linspace(0, 2, 5))
    >>> m.p.shape
    (2, 50)

    """

    refdom = "quad"
    brefdom = "line"
    meshio_type = "quad"

    p = np.array([])
    t = np.array([])
    facets = np.array([])
    f2t = np.array([])
    t2f = np.array([])

    def __init__(self,
                 p: Optional[ndarray] = None,
                 t: Optional[ndarray] = None,
                 validate: Optional[bool] = True):
        """Initialise a quadrilateral mesh.

        Parameters
        ----------
        p
            The points of the mesh (2 x Nvertices).
        t
            The element connectivity (4 x Nelems), i.e. indices to p.
            These should be in counter-clockwise order.

        """
        if p is None and t is None:
            p = np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.]]).T
            t = np.array([[0, 1, 2, 3]]).T
        elif p is None or t is None:
            raise Exception("Must provide p AND t or neither")
        self.p = p
        self.t = t
        if validate:
            self._validate()
        self._build_mappings()
        super(MeshQuad, self).__init__()

    @classmethod
    def init_tensor(cls: Type[MeshType],
                    x: ndarray,
                    y: ndarray) -> MeshType:
        """Initialise a tensor product mesh.

        Parameters
        ----------
        x : numpy array (1d)
            The nodal coordinates in dimension x
        y : numpy array (1d)
            The nodal coordinates in dimension y

        """
        npx = len(x)
        npy = len(y)
        X, Y = np.meshgrid(np.sort(x), np.sort(y))   
        p = np.vstack((X.flatten('F'), Y.flatten('F')))
        ix = np.arange(npx*npy)
        ne = (npx-1)*(npy-1)
        t = np.zeros((4, ne))
        ix = ix.reshape(npy, npx, order='F').copy()
        t[0, :] = ix[0:(npy-1), 0:(npx-1)].reshape(ne, 1, order='F').copy().flatten()
        t[1, :] = ix[1:npy, 0:(npx-1)].reshape(ne, 1, order='F').copy().flatten()
        t[2, :] = ix[1:npy, 1:npx].reshape(ne, 1, order='F').copy().flatten()
        t[3, :] = ix[0:(npy-1), 1:npx].reshape(ne, 1, order='F').copy().flatten()
        return cls(p, t.astype(np.int64))

    @classmethod
    def init_refdom(cls: Type[MeshType]) -> MeshType:
        """Initialise a mesh that includes only the reference quad.
        
        The mesh topology is as follows::

             (-1,1) *-------------* (1,1)
                    |             |
                    |             |
                    |             |
                    |             | 
                    |             | 
                    |             |
                    |             |  
            (-1,-1) *-------------* (1,-1)

        """
        p = np.array([[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]]).T
        t = np.array([[0, 1, 2, 3]]).T
        return cls(p, t)

    def _build_mappings(self):
        # do not sort since order defines counterclockwise order
        # self.t=np.sort(self.t,axis=0)

        # define facets: in the order (0,1) (1,2) (2,3) (0,3)
        self.facets = np.sort(np.vstack((self.t[0, :], self.t[1, :])), axis=0)
        self.facets = np.hstack((self.facets,
                                 np.sort(np.vstack((self.t[1, :],
                                                    self.t[2, :])), axis=0)))
        self.facets = np.hstack((self.facets,
                                 np.sort(np.vstack((self.t[2, :],
                                                    self.t[3, :])), axis=0)))
        self.facets = np.hstack((self.facets,
                                 np.sort(np.vstack((self.t[0, :],
                                                    self.t[3, :])), axis=0)))

        # get unique facets and build quad-to-facet mapping: 4 (edges) x Nquads
        tmp = np.ascontiguousarray(self.facets.T)
        tmp, ixa, ixb = np.unique(tmp.view([('', tmp.dtype)]*tmp.shape[1]),
                                  return_index=True, return_inverse=True)
        self.facets = self.facets[:, ixa]
        self.t2f = ixb.reshape((4, self.t.shape[1]))

        # build facet-to-quadrilateral mapping: 2 (quads) x Nedges
        e_tmp = np.hstack((self.t2f[0, :],
                           self.t2f[1, :],
                           self.t2f[2, :],
                           self.t2f[3, :]))
        t_tmp = np.tile(np.arange(self.t.shape[1]), (1, 4))[0]

        e_first, ix_first = np.unique(e_tmp, return_index=True)
        # this emulates matlab unique(e_tmp,'last')
        e_last, ix_last = np.unique(e_tmp[::-1], return_index=True)
        ix_last = e_tmp.shape[0] - ix_last - 1

        self.f2t = np.zeros((2, self.facets.shape[1]), dtype=np.int64)
        self.f2t[0, e_first] = t_tmp[ix_first]
        self.f2t[1, e_last] = t_tmp[ix_last]

        # second row to -1 if repeated (i.e., on boundary)
        self.f2t[1, np.nonzero(self.f2t[0, :] == self.f2t[1, :])[0]] = -1

    def _uniform_refine(self):
        """Perform a single mesh refine that halves 'h'. Each
        quadrilateral is split into four."""
        # rename variables
        t = self.t
        p = self.p
        e = self.facets
        sz = p.shape[1]
        t2f = self.t2f + sz
        # quadrilateral middle point
        mid = range(self.t.shape[1]) + np.max(t2f) + 1
        # new vertices are the midpoints of edges ...
        newp1 = 0.5*np.vstack((p[0, e[0, :]] + p[0, e[1, :]],
                               p[1, e[0, :]] + p[1, e[1, :]]))
        # ... and element middle points
        newp2 = 0.25*np.vstack((p[0, t[0, :]] + p[0, t[1, :]] +
                                p[0, t[2, :]] + p[0, t[3, :]],
                                p[1, t[0, :]] + p[1, t[1, :]] +
                                p[1, t[2, :]] + p[1, t[3, :]]))
        newp = np.hstack((p, newp1, newp2))
        # build new quadrilateral definitions
        newt = np.vstack((t[0, :],
                          t2f[0, :],
                          mid,
                          t2f[3, :]))
        newt = np.hstack((newt, np.vstack((t2f[0, :],
                                           t[1, :],
                                           t2f[1, :],
                                           mid))))
        newt = np.hstack((newt, np.vstack((mid,
                                           t2f[1, :],
                                           t[2, :],
                                           t2f[2, :]))))
        newt = np.hstack((newt, np.vstack((t2f[3, :],
                                           mid,
                                           t2f[2, :],
                                           t[3, :]))))
        # update fields
        self.p = newp
        self.t = newt

        self._build_mappings()

        # TODO implement prolongation

    def _splitquads(self, x=None):
        """Split each quad into two triangles and return MeshTri."""
        t = self.t[[0, 1, 3], :]
        t = np.hstack((t, self.t[[1, 2, 3]]))

        if x is not None:
            if len(x) == self.t.shape[1]:
                # preserve elemental constant functions
                X = np.concatenate((x, x))
            else:
                raise Exception("The parameter x must have one value per element.")
            return MeshTri(self.p, t, validate=False), X
        else:
            return MeshTri(self.p, t, validate=False)

    def _splitquads_symmetric(self):
        """Split quads into four triangles."""
        t = np.vstack((self.t, np.arange(self.t.shape[1]) + self.p.shape[1]))
        newt = t[[0, 1, 4], :]
        newt = np.hstack((newt, t[[1, 2, 4], :]))
        newt = np.hstack((newt, t[[2, 3, 4], :]))
        newt = np.hstack((newt, t[[3, 0, 4], :]))
        mx = np.sum(self.p[0, self.t], axis=0)/self.t.shape[0]
        my = np.sum(self.p[1, self.t], axis=0)/self.t.shape[0]
        return MeshTri(np.hstack((self.p, np.vstack((mx, my)))), newt, validate=False)

    def plot(self, z, smooth=False, edgecolors=None, ax=None, zlim=None):
        """Visualise piecewise-linear or piecewise-constant function.

        The quadrilaterals are split into two triangles
        (:class:`skfem.mesh.MeshTri`) and the respective plotting function for
        the triangular mesh is used.

        """
        if len(z) == self.t.shape[-1]:
            m, z = self._splitquads(z)
        else:
            m = self._splitquads()
        return m.plot(z, smooth, ax=ax, zlim=zlim, edgecolors=edgecolors)

    def plot3(self, z, smooth=False, ax=None):
        """Visualise nodal function (3d i.e. three axes).

        The quadrilateral mesh is split into triangular mesh (MeshTri)
        and the respective plotting function for the triangular mesh is
        used.

        """
        m, z = self._splitquads(z)
        return m.plot3(z, smooth, ax=ax)

    def mapping(self):
        return skfem.mapping.MappingIsoparametric(self, skfem.element.ElementQuad1(), skfem.element.ElementLineP1())


class MeshHex(Mesh3D):
    """A mesh consisting of hexahedral elements.

    Attributes
    ----------
    p : numpy array of size 3 x Nvertices
        The vertices of the mesh. Each column corresponds to a point.
    t : numpy array of size 8 x Nelements
        The element connectivity. Each column corresponds to a element
        and contains eight column indices to MeshHex.p.
    facets : numpy array of size 4 x Nfacets
        Each column contains four column indices to MeshHex.p.
    f2t : numpy array of size 2 x Nfacets
        Each column contains a pair of column indices to MeshHex.t
        or -1 on the second row if the corresponding
        facet is located on the boundary.
    t2f : numpy array of size 6 x Nelements
        Each column contains four indices to MeshHex.facets.
    edges : numpy array of size 2 x Nedges
        Each column corresponds to an edge and contains two indices to
        MeshHex.p.
    t2e : numpy array of size 12 x Nelements
        Each column contains twelve column indices of MeshHex.edges.

    """

    refdom = "hex"
    brefdom = "quad"
    meshio_type = "hexahedron"

    def __init__(self, p=None, t=None, validate=True):
        """Initialise a hexahedral mesh."""
        if p is None and t is None:
            p = np.array([[0., 0., 0.], [0., 0., 1.], [0., 1., 0.], [1., 0., 0.],
                          [0., 1., 1.], [1., 0., 1.], [1., 1., 0.], [1., 1., 1.]]).T
            t = np.array([[0, 1, 2, 3, 4, 5, 6, 7]]).T
        elif p is None or t is None:
            raise Exception("Must provide p AND t or neither")
        #
        # TODO fix orientation if p and t is provided. refer to
        # the default mesh for correct orientation
        #
        #   2---6
        #  /   /|
        # 4---7 3
        # |   |/
        # 1---5
        #
        # The hidden node is 0.
        #
        self.p = p
        self.t = t
        if validate:
            self._validate()
        self._build_mappings()
        super(MeshHex, self).__init__()

    @classmethod
    def init_tensor(cls: Type[MeshType],
                    x: ndarray,
                    y: ndarray,
                    z: ndarray) -> MeshType:
        """Initialise a tensor product mesh.

        Parameters
        ----------
        x : numpy array (1d)
            The nodal coordinates in dimension x
        y : numpy array (1d)
            The nodal coordinates in dimension y
        z : numpy array (1d)
            The nodal coordinates in dimension z

        """
        npx = len(x)
        npy = len(y)
        npz = len(z)
        X, Y, Z = np.meshgrid(np.sort(x), np.sort(y), np.sort(z))   
        p = np.vstack((X.flatten('F'), Y.flatten('F'), Z.flatten('F')))
        ix = np.arange(npx*npy*npz)
        ne = (npx-1)*(npy-1)*(npz-1)
        t = np.zeros((8, ne))
        ix = ix.reshape(npy, npx, npz, order='F').copy()
        t[0, :] = ix[0:(npy-1), 0:(npx-1), 0:(npz-1)].reshape(ne, 1, order='F').copy().flatten()
        t[1, :] = ix[1:npy, 0:(npx-1), 0:(npz-1)].reshape(ne, 1, order='F').copy().flatten()
        t[2, :] = ix[0:(npy-1), 1:npx, 0:(npz-1)].reshape(ne, 1, order='F').copy().flatten()
        t[3, :] = ix[0:(npy-1), 0:(npx-1), 1:npz].reshape(ne, 1, order='F').copy().flatten()
        t[4, :] = ix[1:npy, 1:npx, 0:(npz-1)].reshape(ne, 1, order='F').copy().flatten()
        t[5, :] = ix[1:npy, 0:(npx-1), 1:npz].reshape(ne, 1, order='F').copy().flatten()
        t[6, :] = ix[0:(npy-1), 1:npx, 1:npz].reshape(ne, 1, order='F').copy().flatten()
        t[7, :] = ix[1:npy, 1:npx, 1:npz].reshape(ne, 1, order='F').copy().flatten()
        return cls(p, t.astype(np.int64))

    def _build_mappings(self):
        """Build element-to-facet, element-to-edges, etc. mappings."""
        self.edges = np.sort(np.vstack((self.t[0, :], self.t[1, :])), axis=0)
        e = np.array([0, 2,
                      0, 3,
                      1, 4,
                      1, 5,
                      2, 4,
                      2, 6,
                      3, 5,
                      3, 6,
                      4, 7,
                      5, 7,
                      6, 7]) # see the picture in init
        for i in range(11):
            self.edges = np.hstack((self.edges, np.sort(np.vstack((self.t[e[2*i], :],
                                                                   self.t[e[2*i+1], :])), axis=0)))

        # unique edges
        self.edges, ixa, ixb = np.unique(self.edges, axis=1, return_index=True, return_inverse=True)
        self.edges = np.ascontiguousarray(self.edges)

        self.t2e = ixb.reshape((12, self.t.shape[1]))

        # define facets
        self.facets = np.vstack((self.t[0, :],
                                 self.t[1, :],
                                 self.t[4, :],
                                 self.t[2, :]))
        f = np.array([0, 2, 6, 3,
                      0, 3, 5, 1,
                      2, 4, 7, 6,
                      1, 5, 7, 4,
                      3, 6, 7, 5])
        for i in range(5):
            self.facets = np.hstack((self.facets, np.vstack((self.t[f[4*i], :],
                                                             self.t[f[4*i+1], :],
                                                             self.t[f[4*i+2], :],
                                                             self.t[f[4*i+3], :]))))

        sorted_facets = np.sort(self.facets, axis=0)

        # unique facets
        sorted_facets, ixa, ixb = np.unique(sorted_facets, axis=1, return_index=True, return_inverse=True)
        self.facets = np.ascontiguousarray(self.facets[:, ixa])

        self.t2f = ixb.reshape((6, self.t.shape[1]))

        # build facet-to-hexa mapping: 2 (hexes) x Nfacets
        e_tmp = np.hstack((self.t2f[0, :], self.t2f[1, :],
                           self.t2f[2, :], self.t2f[3, :],
                           self.t2f[4, :], self.t2f[5, :]))
        t_tmp = np.tile(np.arange(self.t.shape[1]), (1, 6))[0]

        e_first, ix_first = np.unique(e_tmp, return_index=True)
        e_last, ix_last = np.unique(e_tmp[::-1], return_index=True)
        ix_last = e_tmp.shape[0] - ix_last - 1

        self.f2t = np.zeros((2, self.facets.shape[1]), dtype=np.int64)
        self.f2t[0, e_first] = t_tmp[ix_first]
        self.f2t[1, e_last] = t_tmp[ix_last]

        ## second row to zero if repeated (i.e., on boundary)
        self.f2t[1, np.nonzero(self.f2t[0, :] == self.f2t[1, :])[0]] = -1

    def _uniform_refine(self):
        """Perform a single mesh refine that halves 'h'. Each hex is
        split into 8."""
        # rename variables
        t = self.t
        p = self.p
        e = self.edges
        f = self.facets
        sz = p.shape[1]
        t2e = self.t2e + sz
        t2f = self.t2f + np.max(t2e) + 1
        # hex middle point
        mid = range(self.t.shape[1]) + np.max(t2f) + 1
        # new vertices are the midpoints of edges ...
        newp1 = 0.5*np.vstack((p[0, e[0, :]] + p[0, e[1, :]],
                               p[1, e[0, :]] + p[1, e[1, :]],
                               p[2, e[0, :]] + p[2, e[1, :]]))
        # ... midpoints of facets ...
        newp2 = 0.25*np.vstack((p[0, f[0, :]] + p[0, f[1, :]] +
                                p[0, f[2, :]] + p[0, f[3, :]],
                                p[1, f[0, :]] + p[1, f[1, :]] +
                                p[1, f[2, :]] + p[1, f[3, :]],
                                p[2, f[0, :]] + p[2, f[1, :]] +
                                p[2, f[2, :]] + p[2, f[3, :]]))
        # ... and element middle points
        newp3 = 0.125*np.vstack((p[0, t[0, :]] + p[0, t[1, :]] +
                                 p[0, t[2, :]] + p[0, t[3, :]] +
                                 p[0, t[4, :]] + p[0, t[5, :]] +
                                 p[0, t[6, :]] + p[0, t[7, :]],
                                 p[1, t[0, :]] + p[1, t[1, :]] +
                                 p[1, t[2, :]] + p[1, t[3, :]] +
                                 p[1, t[4, :]] + p[1, t[5, :]] +
                                 p[1, t[6, :]] + p[1, t[7, :]],
                                 p[2, t[0, :]] + p[2, t[1, :]] +
                                 p[2, t[2, :]] + p[2, t[3, :]] +
                                 p[2, t[4, :]] + p[2, t[5, :]] +
                                 p[2, t[6, :]] + p[2, t[7, :]]))
        newp = np.hstack((p, newp1, newp2, newp3))
        # build new hex indexing (this requires some serious meditation)
        newt = np.vstack((t[0, :],
                          t2e[0, :],
                          t2e[1, :],
                          t2e[2, :],
                          t2f[0, :],
                          t2f[2, :],
                          t2f[1, :],
                          mid))
        newt = np.hstack((newt, np.vstack((t2e[0, :],
                                           t[1, :],
                                           t2f[0, :],
                                           t2f[2, :],
                                           t2e[3, :],
                                           t2e[4, :],
                                           mid,
                                           t2f[4, :]))))
        newt = np.hstack((newt, np.vstack((t2e[1, :],
                                           t2f[0, :],
                                           t[2, :],
                                           t2f[1, :],
                                           t2e[5, :],
                                           mid,
                                           t2e[6, :],
                                           t2f[3, :]
                                           ))))
        newt = np.hstack((newt, np.vstack((t2e[2, :],
                                           t2f[2, :],
                                           t2f[1, :],
                                           t[3, :],
                                           mid,
                                           t2e[7, :],
                                           t2e[8, :],
                                           t2f[5, :]
                                           ))))
        newt = np.hstack((newt, np.vstack((t2f[0, :],
                                           t2e[3, :],
                                           t2e[5, :],
                                           mid,
                                           t[4, :],
                                           t2f[4, :],
                                           t2f[3, :],
                                           t2e[9, :]
                                           ))))
        newt = np.hstack((newt, np.vstack((t2f[2, :],
                                           t2e[4, :],
                                           mid,
                                           t2e[7, :],
                                           t2f[4, :],
                                           t[5, :],
                                           t2f[5, :],
                                           t2e[10, :],
                                           ))))
        newt = np.hstack((newt, np.vstack((t2f[1, :],
                                           mid,
                                           t2e[6, :],
                                           t2e[8, :],
                                           t2f[3, :],
                                           t2f[5, :],
                                           t[6, :],
                                           t2e[11, :]
                                           ))))
        newt = np.hstack((newt, np.vstack((mid,
                                           t2f[4, :],
                                           t2f[3, :],
                                           t2f[5, :],
                                           t2e[9, :],
                                           t2e[10, :],
                                           t2e[11, :],
                                           t[7, :]
                                           ))))
        # update fields
        self.p = newp
        self.t = newt

        self._build_mappings()

        # TODO implement prolongation

    def save(self,
            filename: str,
            pointData: Optional[Union[ndarray, Dict[str, ndarray]]] = None,
            cellData: Optional[Union[ndarray, Dict[str, ndarray]]] = None):
        """Export the mesh and fields using meshio. (Hexahedron version.)

        Parameters
        ----------
        filename
            The filename for vtk-file.
        pointData
            ndarray for one output or dict for multiple
        cellData
            ndarray for one output or dict for multiple

        """
        import meshio

        # vtk requires a different ordering
        t = self.t[[0, 3, 6, 2, 1, 5, 7, 4], :]

        if pointData is not None:
            if type(pointData) != dict:
                pointData = {'0':pointData}

        if cellData is not None:
            if type(cellData) != dict:
                cellData = {'0':cellData}

        cells = { 'hexahedron' : t.T }
        mesh = meshio.Mesh(self.p.T, cells, pointData, cellData)
        meshio.write(filename, mesh)

    def mapping(self):
        return skfem.mapping.MappingIsoparametric(self, skfem.element.ElementHex1(), skfem.element.ElementQuad1())


class MeshTet(Mesh3D):
    """A mesh consisting of tetrahedral elements.

    Attributes
    ----------
    p : ndarray
        The vertices of the mesh (3 x Nvertices). Each column
        corresponds to a point.
    t : ndarray
        The element connectivity (4 x Nelements). Each column
        corresponds to a element and contains four column indices to
        MeshTet.p.
    facets : ndarray
        Each column contains a triplet of column indices to MeshTet.p
        (3 x Nfacets).  Order: (0, 1, 2) (0, 1, 3) (0, 2, 3) (1, 2, 3)
    f2t : ndarray
        Each column contains a pair of column indices to MeshTet.t or
        -1 on the second row if the facet is located on the boundary
        (2 x Nfacets).
    t2f : ndarray
        Each column contains four indices to MeshTet.facets (4 x Nelements).
    edges : ndarray
        Each column corresponds to an edge and contains two indices to
        MeshTet.p (2 x Nedges).
        Order: (0, 1) (1, 2) (0, 2) (0, 3) (1, 3) (2, 3)
    t2e : ndarray
        Each column contains six indices to MeshTet.edges (6 x Nelements).

    """

    refdom = "tet"
    brefdom = "tri"
    meshio_type = "tetra"

    def __init__(self, p=None, t=None, validate=True):
        if p is None and t is None:
            p = np.array([[0., 0., 0.], [0., 0., 1.], [0., 1., 0.], [1., 0., 0.],
                          [0., 1., 1.], [1., 0., 1.], [1., 1., 0.], [1., 1., 1.]]).T
            t = np.array([[0, 1, 2, 3], [3, 5, 1, 7], [2, 3, 6, 7],
                          [2, 3, 1, 7], [1, 2, 4, 7]]).T
        elif p is None or t is None:
            raise Exception("Must provide p AND t or neither")
        self.p = p
        self.t = t
        if validate:
            self._validate()
        self.enable_facets = True
        self._build_mappings()
        super(MeshTet, self).__init__()

    @classmethod
    def init_tensor(cls: Type[MeshType],
                    x: ndarray,
                    y: ndarray,
                    z: ndarray) -> MeshType:
        """Initialise a tensor product mesh.

        Parameters
        ----------
        x
            The nodal coordinates in dimension x
        y
            The nodal coordinates in dimension y
        z
            The nodal coordinates in dimension z

        License
        -------

        From: https://github.com/nschloe/meshzoo

        Copyright (c) 2016-2018 Nico Schlömer

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.

        """
        # Create the vertices.
        nx, ny, nz = len(x), len(y), len(z)
        x, y, z = np.meshgrid(x, y, z, indexing='ij')
        p = np.array([x, y, z]).T.reshape(-1, 3).T

        # Create the elements.
        a0 = np.add.outer(np.array(range(nx - 1)), nx*np.array(range(ny - 1)))
        a = np.add.outer(a0, nx*ny*np.array(range(nz - 1)))

        elems0 = np.concatenate([a[..., None],
                                 a[..., None] + nx,
                                 a[..., None] + 1,
                                 a[..., None] + nx*ny], axis=3)

        elems0[1::2, 0::2, 0::2, 0] += 1
        elems0[0::2, 1::2, 0::2, 0] += 1
        elems0[0::2, 0::2, 1::2, 0] += 1
        elems0[1::2, 1::2, 1::2, 0] += 1

        elems0[1::2, 0::2, 0::2, 1] += 1
        elems0[0::2, 1::2, 0::2, 1] += 1
        elems0[0::2, 0::2, 1::2, 1] += 1
        elems0[1::2, 1::2, 1::2, 1] += 1

        elems0[1::2, 0::2, 0::2, 2] -= 1
        elems0[0::2, 1::2, 0::2, 2] -= 1
        elems0[0::2, 0::2, 1::2, 2] -= 1
        elems0[1::2, 1::2, 1::2, 2] -= 1

        elems0[1::2, 0::2, 0::2, 3] += 1
        elems0[0::2, 1::2, 0::2, 3] += 1
        elems0[0::2, 0::2, 1::2, 3] += 1
        elems0[1::2, 1::2, 1::2, 3] += 1

        elems1 = np.concatenate([a[..., None] + nx,
                                 a[..., None] + 1 + nx,
                                 a[..., None] + 1,
                                 a[..., None] + 1 + nx + nx*ny], axis=3)

        elems1[1::2, 0::2, 0::2, 0] += 1
        elems1[0::2, 1::2, 0::2, 0] += 1
        elems1[0::2, 0::2, 1::2, 0] += 1
        elems1[1::2, 1::2, 1::2, 0] += 1

        elems1[1::2, 0::2, 0::2, 1] -= 1
        elems1[0::2, 1::2, 0::2, 1] -= 1
        elems1[0::2, 0::2, 1::2, 1] -= 1
        elems1[1::2, 1::2, 1::2, 1] -= 1

        elems1[1::2, 0::2, 0::2, 2] -= 1
        elems1[0::2, 1::2, 0::2, 2] -= 1
        elems1[0::2, 0::2, 1::2, 2] -= 1
        elems1[1::2, 1::2, 1::2, 2] -= 1

        elems1[1::2, 0::2, 0::2, 3] -= 1
        elems1[0::2, 1::2, 0::2, 3] -= 1
        elems1[0::2, 0::2, 1::2, 3] -= 1
        elems1[1::2, 1::2, 1::2, 3] -= 1

        elems2 = np.concatenate([a[..., None] + nx,
                                 a[..., None] + 1,
                                 a[..., None] + nx*ny,
                                 a[..., None] + 1 + nx + nx*ny], axis=3)

        elems2[1::2, 0::2, 0::2, 0] += 1
        elems2[0::2, 1::2, 0::2, 0] += 1
        elems2[0::2, 0::2, 1::2, 0] += 1
        elems2[1::2, 1::2, 1::2, 0] += 1

        elems2[1::2, 0::2, 0::2, 1] -= 1
        elems2[0::2, 1::2, 0::2, 1] -= 1
        elems2[0::2, 0::2, 1::2, 1] -= 1
        elems2[1::2, 1::2, 1::2, 1] -= 1

        elems2[1::2, 0::2, 0::2, 2] += 1
        elems2[0::2, 1::2, 0::2, 2] += 1
        elems2[0::2, 0::2, 1::2, 2] += 1
        elems2[1::2, 1::2, 1::2, 2] += 1

        elems2[1::2, 0::2, 0::2, 3] -= 1
        elems2[0::2, 1::2, 0::2, 3] -= 1
        elems2[0::2, 0::2, 1::2, 3] -= 1
        elems2[1::2, 1::2, 1::2, 3] -= 1

        elems3 = np.concatenate([a[..., None] + nx,
                                 a[..., None] + nx*ny,
                                 a[..., None] + nx + nx*ny,
                                 a[..., None] + 1 + nx + nx*ny], axis=3)

        elems3[1::2, 0::2, 0::2, 0] += 1
        elems3[0::2, 1::2, 0::2, 0] += 1
        elems3[0::2, 0::2, 1::2, 0] += 1
        elems3[1::2, 1::2, 1::2, 0] += 1

        elems3[1::2, 0::2, 0::2, 1] += 1
        elems3[0::2, 1::2, 0::2, 1] += 1
        elems3[0::2, 0::2, 1::2, 1] += 1
        elems3[1::2, 1::2, 1::2, 1] += 1

        elems3[1::2, 0::2, 0::2, 2] += 1
        elems3[0::2, 1::2, 0::2, 2] += 1
        elems3[0::2, 0::2, 1::2, 2] += 1
        elems3[1::2, 1::2, 1::2, 2] += 1

        elems3[1::2, 0::2, 0::2, 3] -= 1
        elems3[0::2, 1::2, 0::2, 3] -= 1
        elems3[0::2, 0::2, 1::2, 3] -= 1
        elems3[1::2, 1::2, 1::2, 3] -= 1

        elems4 = np.concatenate([a[..., None] + 1,
                                 a[..., None] + nx*ny,
                                 a[..., None] + 1 + nx + nx*ny,
                                 a[..., None] + 1 + nx*ny], axis=3)

        elems4[1::2, 0::2, 0::2, 0] -= 1
        elems4[0::2, 1::2, 0::2, 0] -= 1
        elems4[0::2, 0::2, 1::2, 0] -= 1
        elems4[1::2, 1::2, 1::2, 0] -= 1

        elems4[1::2, 0::2, 0::2, 1] += 1
        elems4[0::2, 1::2, 0::2, 1] += 1
        elems4[0::2, 0::2, 1::2, 1] += 1
        elems4[1::2, 1::2, 1::2, 1] += 1

        elems4[1::2, 0::2, 0::2, 2] -= 1
        elems4[0::2, 1::2, 0::2, 2] -= 1
        elems4[0::2, 0::2, 1::2, 2] -= 1
        elems4[1::2, 1::2, 1::2, 2] -= 1

        elems4[1::2, 0::2, 0::2, 3] -= 1
        elems4[0::2, 1::2, 0::2, 3] -= 1
        elems4[0::2, 0::2, 1::2, 3] -= 1
        elems4[1::2, 1::2, 1::2, 3] -= 1

        t = np.vstack([elems0.reshape(-1, 4),
                       elems1.reshape(-1, 4),
                       elems2.reshape(-1, 4),
                       elems3.reshape(-1, 4),
                       elems4.reshape(-1, 4)]).T

        p = np.ascontiguousarray(p)
        t = np.ascontiguousarray(t)

        return cls(p, t)

    def _build_mappings(self):
        """Build element-to-facet, element-to-edges, etc. mappings."""
        # define edges: in the order (0,1) (1,2) (0,2) (0,3) (1,3) (2,3)
        self.edges = np.sort(np.vstack((self.t[0, :], self.t[1, :])), axis=0)
        e = np.array([1, 2,
                      0, 2,
                      0, 3,
                      1, 3,
                      2, 3])
        for i in range(5):
            self.edges = np.hstack((self.edges,
                                    np.sort(np.vstack((self.t[e[2*i], :],
                                                       self.t[e[2*i+1], :])),
                                            axis=0)))

        # unique edges
        self.edges, ixa, ixb = np.unique(self.edges, axis=1, return_index=True, return_inverse=True)
        self.edges = np.ascontiguousarray(self.edges)

        self.t2e = ixb.reshape((6, self.t.shape[1]))

        # define facets
        if self.enable_facets:
            self.facets = np.sort(np.vstack((self.t[0, :],
                                             self.t[1, :],
                                             self.t[2, :])), axis=0)
            f = np.array([0, 1, 3,
                          0, 2, 3,
                          1, 2, 3])
            for i in range(3):
                self.facets = np.hstack((self.facets,
                                         np.sort(np.vstack((self.t[f[2*i], :],
                                                            self.t[f[2*i+1], :],
                                                            self.t[f[2*i+2]])),
                                                 axis=0)))

            # unique facets
            self.facets, ixa, ixb = np.unique(self.facets, axis=1, return_index=True, return_inverse=True)
            self.facets = np.ascontiguousarray(self.facets)

            self.t2f = ixb.reshape((4, self.t.shape[1]))

            # build facet-to-tetra mapping: 2 (tets) x Nfacets
            e_tmp = np.hstack((self.t2f[0, :], self.t2f[1, :],
                               self.t2f[2, :], self.t2f[3, :]))
            t_tmp = np.tile(np.arange(self.t.shape[1]), (1, 4))[0]

            e_first, ix_first = np.unique(e_tmp, return_index=True)
            # this emulates matlab unique(e_tmp,'last')
            e_last, ix_last = np.unique(e_tmp[::-1], return_index=True)
            ix_last = e_tmp.shape[0] - ix_last-1

            self.f2t = np.zeros((2, self.facets.shape[1]), dtype=np.int64)
            self.f2t[0, e_first] = t_tmp[ix_first]
            self.f2t[1, e_last] = t_tmp[ix_last]

            # second row to zero if repeated (i.e., on boundary)
            self.f2t[1, np.nonzero(self.f2t[0, :] == self.f2t[1, :])[0]] = -1

    def refine(self, N=None):
        """Refine the mesh, tetrahedral optimization.
        
        Parameters
        ----------
        N : (optional) int
            Perform N refinements.

        """
        if N is None:
            return self._uniform_refine()
        else:
            self.enable_facets = False
            for itr in range(N-1):
                self._uniform_refine()
            self.enable_facets = True
            self._uniform_refine()

    def _uniform_refine(self):
        """Perform a single mesh refine.

        Let the nodes of a tetrahedron be numbered as 0, 1, 2 and 3.
        It is assumed that the edges in self.t2e are given in the order

          I=(0,1), II=(1,2), III=(0,2), IV=(0,3), V=(1,3), VI=(2,3)

        by self._build_mappings(). Let I denote the midpoint of the edge
        (0,1), II denote the midpoint of the edge (1,2), etc. Then each
        tetrahedron is split into eight smaller subtetrahedra as follows.

        The first four subtetrahedra have the following nodes:

          1. (0,I,III,IV)
          2. (1,I,II,V)
          3. (2,II,III,VI)
          4. (3,IV,V,VI)

        The remaining middle-portion of the original tetrahedron consists
        of a union of two mirrored pyramids. This bi-pyramid can be splitted
        into four tetrahedra in a three different ways by connecting the
        midpoints of two opposing edges (there are three different pairs
        of opposite edges).

        For each tetrahedra in the original mesh, we split the bi-pyramid
        in such a way that the connection between the opposite edges
        is shortest. This minimizes the shape-regularity constant of
        the resulting mesh family.

        """
        # rename variables
        t = self.t
        p = self.p
        e = self.edges
        sz = p.shape[1]
        t2e = self.t2e + sz
        # new vertices are the midpoints of edges
        newp = 0.5*np.vstack((p[0, e[0, :]] + p[0, e[1, :]],
                              p[1, e[0, :]] + p[1, e[1, :]],
                              p[2, e[0, :]] + p[2, e[1, :]]))
        newp = np.hstack((p, newp))
        # new tets
        newt = np.vstack((t[0, :], t2e[0, :], t2e[2, :], t2e[3, :]))
        newt = np.hstack((newt, np.vstack((t[1, :], t2e[0, :], t2e[1, :], t2e[4, :]))))
        newt = np.hstack((newt, np.vstack((t[2, :], t2e[1, :], t2e[2, :], t2e[5, :]))))
        newt = np.hstack((newt, np.vstack((t[3, :], t2e[3, :], t2e[4, :], t2e[5, :]))))
        # compute middle pyramid diagonal lengths and choose shortest
        d1 = ((newp[0, t2e[2, :]] - newp[0, t2e[4, :]])**2 +
              (newp[1, t2e[2, :]] - newp[1, t2e[4, :]])**2)
        d2 = ((newp[0, t2e[1, :]] - newp[0, t2e[3, :]])**2 +
              (newp[1, t2e[1, :]] - newp[1, t2e[3, :]])**2)
        d3 = ((newp[0, t2e[0, :]] - newp[0, t2e[5, :]])**2 +
              (newp[1, t2e[0, :]] - newp[1, t2e[5, :]])**2)
        I1 = d1 < d2
        I2 = d1 < d3
        I3 = d2 < d3
        c1 = I1*I2
        c2 = (~I1)*I3
        c3 = (~I2)*(~I3)
        # splitting the pyramid in the middle.
        # diagonals are [2,4], [1,3] and [0,5]
        # CASE 1: diagonal [2,4]
        newt = np.hstack((newt, np.vstack((t2e[2, c1], t2e[4, c1],
                                           t2e[0, c1], t2e[1, c1]))))
        newt = np.hstack((newt, np.vstack((t2e[2, c1], t2e[4, c1],
                                           t2e[0, c1], t2e[3, c1]))))
        newt = np.hstack((newt, np.vstack((t2e[2, c1], t2e[4, c1],
                                           t2e[1, c1], t2e[5, c1]))))
        newt = np.hstack((newt, np.vstack((t2e[2, c1], t2e[4, c1],
                                           t2e[3, c1], t2e[5, c1]))))
        # CASE 2: diagonal [1,3]
        newt = np.hstack((newt, np.vstack((t2e[1, c2], t2e[3, c2],
                                           t2e[0, c2], t2e[4, c2]))))
        newt = np.hstack((newt, np.vstack((t2e[1, c2], t2e[3, c2],
                                           t2e[4, c2], t2e[5, c2]))))
        newt = np.hstack((newt, np.vstack((t2e[1, c2], t2e[3, c2],
                                           t2e[5, c2], t2e[2, c2]))))
        newt = np.hstack((newt, np.vstack((t2e[1, c2], t2e[3, c2],
                                           t2e[2, c2], t2e[0, c2]))))
        # CASE 3: diagonal [0,5]
        newt = np.hstack((newt, np.vstack((t2e[0, c3], t2e[5, c3],
                                           t2e[1, c3], t2e[4, c3]))))
        newt = np.hstack((newt, np.vstack((t2e[0, c3], t2e[5, c3],
                                           t2e[4, c3], t2e[3, c3]))))
        newt = np.hstack((newt, np.vstack((t2e[0, c3], t2e[5, c3],
                                           t2e[3, c3], t2e[2, c3]))))
        newt = np.hstack((newt, np.vstack((t2e[0, c3], t2e[5, c3],
                                           t2e[2, c3], t2e[1, c3]))))
        # update fields
        self.p = newp
        self.t = newt

        self._build_mappings()

        # TODO implement prolongation matrix

    def shapereg(self):
        """Return the largest shape-regularity constant."""
        def edgelen(n):
            return np.sqrt(np.sum((self.p[:, self.edges[0, self.t2e[n, :]]] -
                                   self.p[:, self.edges[1, self.t2e[n, :]]])**2,
                                  axis=0))
        edgelenmat = np.vstack(tuple(edgelen(i) for i in range(6)))
        return np.max(np.max(edgelenmat, axis=0)/np.min(edgelenmat, axis=0))

    def mapping(self):
        return skfem.mapping.MappingAffine(self)


class MeshTri(Mesh2D):
    """A mesh consisting of triangular elements.

    The different constructors are:

        - :meth:`~skfem.mesh.MeshTri.__init__`
        - :meth:`~skfem.mesh.MeshTri.load` (requires meshio)
        - :meth:`~skfem.mesh.MeshTri.init_symmetric`
        - :meth:`~skfem.mesh.MeshTri.init_sqsymmetric`
        - :meth:`~skfem.mesh.MeshTri.init_refdom`
        - :meth:`~skfem.mesh.MeshTri.init_tensor`
    
    Attributes
    ----------
    p
        An array containing the vertices of the mesh (2 x Nvertices).
    t
        An array containing the element connectivity (3 x Nelems).
    facets
        An array containing the facet vertices (2 x Nfacets).
    f2t
        An array containing the triangles next to each facet (2 x Nfacets).
        Each column contains two indices to t.  If the second row is zero then
        the facet is on the boundary.
    t2f
        An array containing the facets belonging to each triangle (3 x Nelems).
        Each column contains three indices to facets.

    Examples
    --------
    Initialise a symmetric mesh of the unit square.

    >>> m = MeshTri.init_sqsymmetric()
    >>> m.t.shape
    (3, 8)

    Facets (edges) and mappings from triangles to facets and vice versa are
    automatically constructed. In the following example we have 5 facets
    (edges).

    >>> m = MeshTri()
    >>> m.facets
    array([[0, 0, 1, 1, 2],
           [1, 2, 2, 3, 3]])
    >>> m.t2f
    array([[0, 2],
           [2, 4],
           [1, 3]])
    >>> m.f2t
    array([[ 0,  0,  1,  1,  1],
           [-1, -1,  0, -1, -1]])

    The value -1 implies that the facet (the edge) is on the boundary.

    Refine the triangular mesh of the unit square three times.

    >>> m = MeshTri()
    >>> m.refine(3)
    >>> m.p.shape
    (2, 81)

    """

    refdom = "tri"
    brefdom = "line"
    meshio_type = "triangle"

    p = np.array([])
    t = np.array([])
    facets = np.array([])
    f2t = np.array([])
    t2f = np.array([])

    def __init__(self,
                 p: Optional[ndarray] = None,
                 t: Optional[ndarray] = None,
                 validate: Optional[bool] = True,
                 sort_t: Optional[bool] = True):
        """Initialise a triangular mesh.

        If no arguments are given, initialises a mesh with the following
        topology::

            *-------------*
            |\            |
            |  \          |
            |    \        |
            |      \      |
            |        \    |
            |          \  |
            |            \|
            *-------------*

        Parameters
        ----------
        p
            An array containing the points of the mesh (2 x Nvertices).
        t
            An array containing the element connectivity (3 x Nelems), i.e.
            indices to p.
        validate
            If true, run mesh validity checks.
        sort_t
            If true, sort the element connectivity matrix before building
            mappings.

        """
        if p is None and t is None:
            p = np.array([[0., 1., 0., 1.], [0., 0., 1., 1.]], dtype=np.float_)
            t = np.array([[0, 1, 2], [1, 3, 2]], dtype=np.intp).T
        elif p is None or t is None:
            raise Exception("Must provide p AND t or neither")
        self.p = p
        self.t = t
        if validate:
            self._validate()
        self._build_mappings(sort_t=sort_t)
        super(MeshTri, self).__init__()

    @classmethod
    def init_tensor(cls: Type[MeshType],
                    x: ndarray,
                    y: ndarray) -> MeshType:
        """Initialise a tensor product mesh.

        Parameters
        ----------
        x
            The nodal coordinates in dimension x.
        y
            The nodal coordinates in dimension y.

        """
        return MeshQuad.init_tensor(x, y)._splitquads()

    @classmethod
    def init_symmetric(cls):
        """Initialise a symmetric mesh of the unit square.
        
        The mesh topology is as follows::

            *------------*
            |\          /|
            |  \      /  |
            |    \  /    |
            |     *      |
            |    /  \    |
            |  /      \  |
            |/          \|
            *------------*

        """
        p = np.array([[0, 1, 1, 0, 0.5],
                      [0, 0, 1, 1, 0.5]], dtype=np.float_)
        t = np.array([[0, 1, 4],
                      [1, 2, 4],
                      [2, 3, 4],
                      [0, 3, 4]], dtype=np.intp).T
        return cls(p, t)

    @classmethod
    def init_sqsymmetric(cls: Type[MeshType]) -> MeshType:
        """Initialise a symmetric mesh of the unit square.
        
        The mesh topology is as follows::

            *------------*
            |\    |     /|
            |  \  |   /  |
            |    \| /    |
            |-----*------|
            |    /| \    |
            |  /  |   \  |
            |/    |     \|
            *------------*

        """
        p = np.array([[0, 0.5, 1,   0, 0.5,   1, 0, 0.5, 1],
                      [0, 0,   0, 0.5, 0.5, 0.5, 1,   1, 1]], dtype=np.float_)
        t = np.array([[0, 1, 4],
                      [1, 2, 4],
                      [2, 4, 5],
                      [0, 3, 4],
                      [3, 4, 6],
                      [4, 6, 7],
                      [4, 7, 8],
                      [4, 5, 8]], dtype=np.intp).T
        return cls(p, t)

    @classmethod
    def init_refdom(cls: Type[MeshType]) -> MeshType:
        """Initialise a mesh that includes only the reference triangle.
        
        The mesh topology is as follows::

            *
            |\           
            |  \         
            |    \       
            |      \      
            |        \    
            |          \  
            |            \ 
            *-------------*

        """
        p = np.array([[0., 1., 0.],
                      [0., 0., 1.]], dtype=np.float_)
        t = np.array([[0, 1, 2]], dtype=np.intp).T
        return cls(p, t)

    def _build_mappings(self, sort_t=True):
        # sort to preserve orientations etc.
        if sort_t:
            self.t = np.sort(self.t, axis=0)

        # define facets: in the order (0,1) (1,2) (0,2)
        self.facets = np.sort(np.vstack((self.t[0, :], self.t[1, :])), axis=0)
        self.facets = np.hstack((self.facets,
                                 np.sort(np.vstack((self.t[1, :], self.t[2, :])),
                                         axis=0)))
        self.facets = np.hstack((self.facets,
                                 np.sort(np.vstack((self.t[0, :], self.t[2, :])),
                                         axis=0)))

        # get unique facets and build triangle-to-facet
        # mapping: 3 (edges) x Ntris
        tmp = np.ascontiguousarray(self.facets.T)
        tmp, ixa, ixb = np.unique(tmp.view([('', tmp.dtype)] * tmp.shape[1]),
                                  return_index=True, return_inverse=True)
        self.facets = self.facets[:, ixa]
        self.t2f = ixb.reshape((3, self.t.shape[1]))

        # build facet-to-triangle mapping: 2 (triangles) x Nedges
        e_tmp = np.hstack((self.t2f[0, :], self.t2f[1, :], self.t2f[2, :]))
        t_tmp = np.tile(np.arange(self.t.shape[1]), (1, 3))[0]

        e_first, ix_first = np.unique(e_tmp, return_index=True)
        # this emulates matlab unique(e_tmp,'last')
        e_last, ix_last = np.unique(e_tmp[::-1], return_index=True)
        ix_last = e_tmp.shape[0] - ix_last - 1

        self.f2t = np.zeros((2, self.facets.shape[1]), dtype=np.int64)
        self.f2t[0, e_first] = t_tmp[ix_first]
        self.f2t[1, e_last] = t_tmp[ix_last]

        # second row to zero if repeated (i.e., on boundary)
        self.f2t[1, np.nonzero(self.f2t[0, :] == self.f2t[1, :])[0]] = -1

    def interpolator(self, x):
        """Return a function which interpolates values with P1 basis."""
        triang = mtri.Triangulation(self.p[0, :], self.p[1, :], self.t.T)
        interpf = mtri.LinearTriInterpolator(triang, x)
        # contruct an interpolator handle
        def handle(X, Y):
            return interpf(X, Y).data
        return handle

    def const_interpolator(self, x):
        """Return a function which interpolates values with P0 basis."""
        triang = mtri.Triangulation(self.p[0, :], self.p[1, :], self.t.T)
        finder = triang.get_trifinder()
        # construct an interpolator handle
        def handle(X, Y):
            return x[finder(X, Y)]
        return handle

    def draw_debug(self):
        """Draw without mesh.facets. For debugging self.draw()."""
        fig = plt.figure()
        plt.hold('on')
        for itr in range(self.t.shape[1]):
            plt.plot(self.p[0,self.t[[0,1],itr]], self.p[1,self.t[[0,1],itr]], 'k-')
            plt.plot(self.p[0,self.t[[1,2],itr]], self.p[1,self.t[[1,2],itr]], 'k-')
            plt.plot(self.p[0,self.t[[0,2],itr]], self.p[1,self.t[[0,2],itr]], 'k-')
        return fig

    def plot(self,
             z: ndarray,
             smooth: Optional[bool] = False,
             ax: Optional[Axes] = None,
             zlim: Optional[Tuple[float, float]] = None,
             edgecolors: Optional[str] = None,
             aspect: float = 1.) -> Axes:
        """Visualise piecewise-linear or piecewise-constant function, 2D plot.
        
        Parameters
        ----------
        z
            An array of nodal values (Nvertices) or elemental values (Nelems).
        smooth
            If true, use gouraud shading.
        ax
            Plot onto the given preinitialised Matplotlib axes.
        zlim
            Use the given minimum and maximum values for coloring.
        edgecolors
            A string describing the edge coloring, e.g. 'k' for black.
        float
            The ratio of vertical to horizontal length-scales; ignored if ax
            specified.

        Returns
        -------
        Axes
            The Matplotlib axes onto which the mesh was plotted.

        Examples
        --------
        Mesh the unit square :math:`(0,1)^2` and visualise the function
        :math:`f(x)=x^2`.

        >>> from skfem.mesh import MeshTri
        >>> m = MeshTri()
        >>> m.refine(3)
        >>> ax = m.plot(m.p[0, :]**2, smooth=True)
        >>> m.show()
        
        .. figure:: pics/api_MeshTri_plot.png
            
        """
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_aspect(aspect)
        if edgecolors is None:
            edgecolors = 'k'
        if zlim == None:
            if smooth:
                ax.tripcolor(self.p[0, :], self.p[1, :], self.t.T, z,
                              shading='gouraud', edgecolors=edgecolors)
            else:
                ax.tripcolor(self.p[0, :], self.p[1, :], self.t.T, z, edgecolors=edgecolors)
        else:
            if smooth:
                ax.tripcolor(self.p[0, :], self.p[1, :], self.t.T, z,
                              shading='gouraud', vmin=zlim[0], vmax=zlim[1], edgecolors=edgecolors)
            else:
                ax.tripcolor(self.p[0, :], self.p[1, :], self.t.T, z,
                              vmin=zlim[0], vmax=zlim[1], edgecolors=edgecolors)
        return ax

    def plot3(self,
              z: ndarray,
              smooth: Optional[bool] = False,
              ax: Optional[Axes] = None) -> Axes:
        """Visualise piecewise-linear or piecewise-constant function, 3D plot.
        
        Parameters
        ----------
        z
            An array of nodal values (Nvertices) or elemental values (Nelems).
        smooth
            If true, use gouraud shading.
        ax
            Plot onto the given preinitialised Matplotlib axes.

        Returns
        -------
        Axes
            The Matplotlib axes onto which the mesh was plotted.
        
        Examples
        --------
        Mesh the unit square :math:`(0,1)^2` and visualise the function
        :math:`f(x)=x^2`.

        >>> from skfem.mesh import MeshTri
        >>> m = MeshTri()
        >>> m.refine(3)
        >>> ax = m.plot3(m.p[1, :]**2)
        >>> m.show()
        
        .. figure:: pics/api_MeshTri_plot3.png
            
        """
        from mpl_toolkits.mplot3d import Axes3D
        if ax is None:
            fig = plt.figure()
            ax = Axes3D(fig)
        if len(z) == self.p.shape[1]:
            # use matplotlib
            ts = mtri.Triangulation(self.p[0, :], self.p[1, :], self.t.T)
            ax.plot_trisurf(self.p[0, :], self.p[1, :], z,
                            triangles=ts.triangles,
                            cmap=plt.cm.Spectral)
        elif len(z) == self.t.shape[1]:
            # one value per element (piecewise const)
            nt = self.t.shape[1]
            newt = np.arange(3*nt, dtype=np.int64).reshape((nt, 3))
            newpx = self.p[0, self.t].flatten(order='F')
            newpy = self.p[1, self.t].flatten(order='F')
            newz = np.vstack((z, z, z)).flatten(order='F')
            ts = mtri.Triangulation(newpx, newpx, newt)
            ax.plot_trisurf(newpx, newpy, newz,
                            triangles=ts.triangles,
                            cmap=plt.cm.Spectral)
        elif len(z) == 3*self.t.shape[1]:
            # three values per element (piecewise linear)
            nt = self.t.shape[1]
            newt = np.arange(3*nt, dtype=np.int64).reshape((nt, 3))
            newpx = self.p[0, self.t].flatten(order='F')
            newpy = self.p[1, self.t].flatten(order='F')
            ts = mtri.Triangulation(newpx, newpx, newt)
            ax.plot_trisurf(newpx, newpy, z,
                            triangles=ts.triangles,
                            cmap=plt.cm.Spectral)
        else:
            raise NotImplementedError("MeshTri.plot3: not implemented for "
                                      "the given shape of input vector!")
        return ax

    def _uniform_refine(self):
        """Perform a single mesh refine."""
        # rename variables
        t = self.t
        p = self.p
        e = self.facets
        sz = p.shape[1]
        t2f = self.t2f + sz
        # new vertices are the midpoints of edges
        newp = 0.5*np.vstack((p[0, e[0, :]] + p[0, e[1, :]],
                              p[1, e[0, :]] + p[1, e[1, :]]))
        newp = np.hstack((p, newp))
        # build new triangle definitions
        newt = np.vstack((t[0, :], t2f[0, :], t2f[2, :]))
        newt = np.hstack((newt, np.vstack((t[1, :], t2f[0, :], t2f[1, :]))))
        newt = np.hstack((newt, np.vstack((t[2, :], t2f[2, :], t2f[1, :]))))
        newt = np.hstack((newt, np.vstack((t2f[0, :], t2f[1, :], t2f[2, :]))))
        # update fields
        self.p = newp
        self.t = newt

        self._build_mappings()

        # prolongation matrix
        nsz = newp.shape[1]
        return coo_matrix(
            (np.hstack((np.ones(sz), .5 * np.ones(2 * (nsz - sz)))),
             (np.hstack((np.arange(sz), np.arange(nsz - sz) + sz, np.arange(nsz - sz) + sz)),
              np.hstack((np.arange(sz), e[0, :], e[1, :])))),
            shape=(nsz, sz)).tocsr()

    def mapping(self):
        return skfem.mapping.MappingAffine(self)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
