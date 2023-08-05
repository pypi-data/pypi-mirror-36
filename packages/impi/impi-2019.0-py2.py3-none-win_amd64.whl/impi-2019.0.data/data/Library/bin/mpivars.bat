@echo off
Rem Intel(R) MPI Library Build Environment

if "%1" == "quiet" (
    shift
    goto EXPORTS
) else if "%2" == "quiet" (
    goto EXPORTS
)

title Intel(R) MPI Library 2019 for Windows* Target Build Environment for Intel(R) 64 applications

echo.
echo Intel(R) MPI Library 2019 for Windows* Target Build Environment for Intel(R) 64 applications
echo Copyright 2007-2018 Intel Corporation.
echo.

:EXPORTS
SET I_MPI_ROOT=%~dp0..\..
SET PATH=%I_MPI_ROOT%\intel64\bin\release;%I_MPI_ROOT%\intel64\bin;%PATH%
SET LIB=%I_MPI_ROOT%\intel64\lib\release;%I_MPI_ROOT%\intel64\lib;%LIB%
SET INCLUDE=%I_MPI_ROOT%\intel64\include;%INCLUDE%

if /i "%1"=="-ofi_internal" set I_MPI_OFI_LIBRARY_INTERNAL=%2& shift& shift
if /i "%1"=="--ofi_internal" set I_MPI_OFI_LIBRARY_INTERNAL=%2& shift& shift

if /i "%1"=="debug" (
    goto EXTRA_EXPORTS
)
if /i "%1"=="release" (
    goto EXTRA_EXPORTS
)
if /i "%1"=="debug_mt" (
    goto EXTRA_EXPORTS
)
if /i "%1"=="release_mt" (
    goto EXTRA_EXPORTS
)
goto NO_EXTRA_EXPORTS

:EXTRA_EXPORTS
set PATH=%I_MPI_ROOT%\intel64\bin\%1;%PATH%
set LIB=%I_MPI_ROOT%\intel64\lib\%1;%LIB%

:NO_EXTRA_EXPORTS

if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="0" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="no" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="off" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="disable" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="1" goto SET_LIBFABRIC_PATH
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="yes" goto SET_LIBFABRIC_PATH
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="on" goto SET_LIBFABRIC_PATH
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="enable" goto SET_LIBFABRIC_PATH

where libfabric.dll >nul 2>&1
if not "%errorlevel%"=="0" goto SET_LIBFABRIC_PATH

"%I_MPI_ROOT%\intel64\libfabric\bin\utils\fi_info.exe" --version >nul 2>&1
if not "%errorlevel%"=="0" goto SET_LIBFABRIC_PATH

where fi_info.exe >nul 2>&1
if not "%errorlevel%"=="0" set PATH=%I_MPI_ROOT%\intel64\libfabric\bin\utils;%PATH%

goto :EOF

:SET_LIBFABRIC_PATH
set PATH=%I_MPI_ROOT%\intel64\libfabric\bin\utils;%I_MPI_ROOT%\intel64\libfabric\bin;%PATH%

