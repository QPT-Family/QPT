# Author: Acer Zhang
# Datetime:2021/7/7 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import sys
import traceback
from qpt.kernel.qos import Logging

SUPPORT_AVX = None
try:
    from paddle.fluid.core_avx import *
    from paddle.fluid.core_avx import __doc__, __file__, __name__, __package__
    from paddle.fluid.core_avx import __unittest_throw_exception__
    from paddle.fluid.core_avx import _append_python_callable_object_and_return_id
    from paddle.fluid.core_avx import _cleanup, _Scope
    from paddle.fluid.core_avx import _get_use_default_grad_op_desc_maker_ops
    from paddle.fluid.core_avx import _get_all_register_op_kernels
    from paddle.fluid.core_avx import _is_program_version_supported
    from paddle.fluid.core_avx import _set_eager_deletion_mode
    from paddle.fluid.core_avx import _set_fuse_parameter_group_size
    from paddle.fluid.core_avx import _set_fuse_parameter_memory_size
    from paddle.fluid.core_avx import _is_dygraph_debug_enabled
    from paddle.fluid.core_avx import _dygraph_debug_level
    from paddle.fluid.core_avx import _switch_tracer
    from paddle.fluid.core_avx import _set_paddle_lib_path
    from paddle.fluid.core_avx import _save_static_dict
    from paddle.fluid.core_avx import _load_static_dict
    from paddle.fluid.core_avx import _save_dygraph_dict
    from paddle.fluid.core_avx import _load_dygraph_dict
    from paddle.fluid.core_avx import _save_lod_tensor
    from paddle.fluid.core_avx import _load_lod_tensor
    from paddle.fluid.core_avx import _save_selected_rows
    from paddle.fluid.core_avx import _load_selected_rows
    from paddle.fluid.core_avx import _create_loaded_parameter
    from paddle.fluid.core_avx import _cuda_synchronize
    from paddle.fluid.core_avx import _promote_types_if_complex_exists

    if sys.platform != 'win32':
        from paddle.fluid.core_avx import _set_process_pids
        from paddle.fluid.core_avx import _erase_process_pids
        from paddle.fluid.core_avx import _set_process_signal_handler
        from paddle.fluid.core_avx import _throw_error_if_process_failed
        from paddle.fluid.core_avx import _convert_to_tensor_list
        from paddle.fluid.core_avx import _array_to_share_memory_tensor
        from paddle.fluid.core_avx import _cleanup_mmap_fds
        from paddle.fluid.core_avx import _remove_tensor_list_mmap_fds
    SUPPORT_AVX = True
except Exception as e:
    Logging.warning(str(e))
    info = traceback.format_exc()
    if "cv2" in info:
        # ToDo 实际上还是不能确定，但Paddle这块不知道为什么要这样测cv2是否存在
        SUPPORT_AVX = True
    else:
        SUPPORT_AVX = False
