from cupy.sparse.base import issparse  # NOQA
from cupy.sparse.base import isspmatrix  # NOQA
from cupy.sparse.base import spmatrix  # NOQA
from cupy.sparse.coo import coo_matrix  # NOQA
from cupy.sparse.coo import isspmatrix_coo  # NOQA
from cupy.sparse.csc import csc_matrix  # NOQA
from cupy.sparse.csc import isspmatrix_csc  # NOQA
from cupy.sparse.csr import csr_matrix  # NOQA
from cupy.sparse.csr import isspmatrix_csr  # NOQA
from cupy.sparse.dia import dia_matrix  # NOQA
from cupy.sparse.dia import isspmatrix_dia  # NOQA

from cupy.sparse.construct import eye  # NOQA
from cupy.sparse.construct import identity  # NOQA
from cupy.sparse.construct import rand  # NOQA
from cupy.sparse.construct import random  # NOQA
from cupy.sparse.construct import spdiags  # NOQA

# TODO(unno): implement bsr_matrix
# TODO(unno): implement dok_matrix
# TODO(unno): implement lil_matrix

# TODO(unno): implement kron
# TODO(unno): implement kronsum
# TODO(unno): implement diags
# TODO(unno): implement block_diag
# TODO(unno): implement tril
# TODO(unno): implement triu
# TODO(unno): implement bmat
# TODO(unno): implement hstack
# TODO(unno): implement vstack

# TODO(unno): implement save_npz
# TODO(unno): implement load_npz

# TODO(unno): implement find

# TODO(unno): implement isspmatrix_bsr(x)
# TODO(unno): implement isspmatrix_lil(x)
# TODO(unno): implement isspmatrix_dok(x)

from cupy.sparse import linalg  # NOQA
