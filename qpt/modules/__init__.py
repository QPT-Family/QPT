import platform


def check_bit():
    arc = platform.machine()
    assert "64" in arc, "当前QPT不支持32位操作系统"


def check_os():
    p_os = platform.system()
    if p_os is None:
        return 0
    assert "Windows" in p_os, "当前QPT只支持Windows系统"


def avx_supported():
    """
    Via: https://github.com/PaddlePaddle/Paddle/blob/develop/python/paddle/fluid/core.py#L71
    """
    import ctypes
    ONE_PAGE = ctypes.c_size_t(0x1000)

    def asm_func(code_str, restype=ctypes.c_uint32, argtypes=()):
        pfnVirtualAlloc = ctypes.windll.kernel32.VirtualAlloc
        pfnVirtualAlloc.restype = ctypes.c_void_p
        MEM_COMMIT = ctypes.c_ulong(0x1000)
        PAGE_READWRITE = ctypes.c_ulong(0x4)
        address = pfnVirtualAlloc(None, ONE_PAGE, MEM_COMMIT,
                                  PAGE_READWRITE)
        if not address:
            raise Exception("Failed to VirtualAlloc")

        # Copy the code into the memory segment
        memmove = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p,
                                   ctypes.c_void_p,
                                   ctypes.c_size_t)(ctypes._memmove_addr)
        if memmove(address, code_str, len(code_str)) < 0:
            raise Exception("Failed to memmove")

        # Enable execute permissions
        PAGE_EXECUTE = ctypes.c_ulong(0x10)
        pfnVirtualProtect = ctypes.windll.kernel32.VirtualProtect
        res = pfnVirtualProtect(
            ctypes.c_void_p(address), ONE_PAGE, PAGE_EXECUTE,
            ctypes.byref(ctypes.c_ulong(0)))
        if not res:
            raise Exception("Failed VirtualProtect")

        # Flush instruction cache
        pfnGetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
        pfnGetCurrentProcess.restype = ctypes.c_void_p
        prochandle = ctypes.c_void_p(pfnGetCurrentProcess())
        res = ctypes.windll.kernel32.FlushInstructionCache(
            prochandle, ctypes.c_void_p(address), ONE_PAGE)
        if not res:
            raise Exception("Failed FlushInstructionCache")

        # Cast the memory to function
        functype = ctypes.CFUNCTYPE(restype, *argtypes)
        func = functype(address)
        return func, address

    code_str = b"\xB8\x01\x00\x00\x00\x0f\xa2\x89\xC8\xC3"
    try:
        # Convert the code_str into a function that returns uint
        func, address = asm_func(code_str)
        ctypes.windll.kernel32.VirtualFree(
            ctypes.c_void_p(address), ctypes.c_size_t(0), ONE_PAGE)
    except Exception as e:
        return False
    return True


check_os()
check_bit()
AVX_SUPPORT = avx_supported()
