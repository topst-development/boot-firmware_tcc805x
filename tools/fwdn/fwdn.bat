@echo off

echo Start the FWDN V8

if "%1" == "-h" goto help

if "%1" == "ubuntu" goto ubuntu

:choose
	echo Enter the part you want to install : all, main, sub, mcu, QUIT
	set /p CORE=: 
	set PART=TEST

	if %CORE%==QUIT (
		goto QUIT
	)
	if %CORE%==all (
		goto preload
	)
	if %CORE%==main (
		echo Enter the part you want to install on main-core?: all, bootloader, kernel, filesystem, dtb, home
		set /p PART=: 
		goto preload
	) 
	if %CORE%==sub (
		echo Enter the part you want to install on sub-core? : all, bootloader, kernel, filesystem, dtb, home
		set /p PART=: 
		goto preload
	) 
	if %CORE%==ubuntu_main (
		goto preload
	)		
	if %CORE%==mcu (
		goto preload
	) else (
		goto help
	)

:preload
	set main-path=deploy-images\tcc8050-main
	set sub-path=deploy-images\tcc8050-sub

	echo Install Start
	if exist %deploy-images\boot-firmware (
		echo Connect FWDN V8 to Board
		fwdn.exe --fwdn deploy-images\boot-firmware\fwdn.json

		if %CORE%==all (
			echo Low-Format eMMC
			fwdn.exe --storage emmc --low-format

			echo Download Pre-built F/W Image
			fwdn.exe -w deploy-images\boot-firmware\boot.json
		)
		goto %CORE%
	) else (
		echo Not exist boot-fimware file
		goto QUIT
	)

:all
	echo.
	echo MCU install
	if exist %deploy-images\cr5_snor.rom (
		fwdn.exe -w deploy-images\cr5_snor.rom --area die1 --storage snor
	)else (
		echo Not exist cr5_snor.rom file
		goto QUIT
	)

	echo.
	echo SD_Data install
	if exist %deploy-images\SD_Data.fai (
		echo Download FAI File - SD_Data.fai
		fwdn.exe -w deploy-images\SD_Data.fai --storage emmc --area user
	)
	exit /b

:main
	if %PART%==all goto all_main

	if %PART%==bootloader goto bootloader

	if %PART%==kernel goto kernel

	if %PART%==filesystem goto filesystem

	if %PART%==dtb goto dtb

	if %PART%==home goto home
	else goto help

:sub
	if %PART%==all goto all_sub

	if %PART%==bootloader goto bootloader_sub

	if %PART%==kernel goto kernel_sub

	if %PART%==filesystem goto filesystem_sub

	if %PART%==dtb goto dtb_sub

	if %PART%==home goto home_sub
	else goto help

:mcu
	echo.
	echo mcu install
	if exist %deploy-images\cr5_snor.rom (
		fwdn.exe -w deploy-images\cr5_snor.rom --area die1 --storage snor
		echo.
		goto choose
	)else (
		echo Not exist boot-fimware file
		goto QUIT
	)

:all_main
	echo.
	echo Boot Loader install for main core
	fwdn.exe -w %main-path%\ca72_bl3.rom --storage emmc --area user --part bl3_ca72_a
	echo.
	echo Kernel install for main core
	fwdn.exe -w %main-path%\tc-boot-tcc8050-main.img --storage emmc --area user --part boot
	echo.
	echo File System install for main core
	fwdn.exe -w %main-path%\automotive-linux-platform-image-tcc8050-main.ext4 --storage emmc --area user --part system
	echo.
	echo DTB install for main core
	fwdn.exe -w %main-path%\tcc8050-linux-ivi-tost_sv0.1.dtb --storage emmc --area user --part dtb
	echo.
	echo Home install for main core
	fwdn.exe -w deploy-images\home-directory.ext4 --storage emmc --area user --part home
	echo.
	goto choose

:all_sub
	echo.
	echo Boot Loader install for sub core
	fwdn.exe -w %sub-path%\ca53_bl3.rom --storage emmc --area user --part bl3_ca53_a 
	echo.
	echo Kernel install for sub core
	fwdn.exe -w %sub-path%\tc-boot-tcc8050-sub.img --storage emmc --area user --part subcore_boot
	echo.
	echo File System install for sub core
	fwdn.exe -w %sub-path%\telechips-subcore-image-tcc8050-sub.ext4 --storage emmc --area user --part subcore_root
	echo.
	echo DTB install for sub core
	fwdn.exe -w %sub-path%\tcc8050-linux-subcore-ivi-tost_sv0.1.dtb --storage emmc --area user --part subcore_dtb
	echo.
	if exist %deploy-images\home-directory.ext4 (		
		echo Home install for sub core
		fwdn.exe -w deploy-images\home-directory.ext4 --storage emmc --area user --part home
		echo.
	)else (
		echo Not exist home-directory.ext4
	)
	goto choose

:bootloader
	echo.
	echo Boot Loader install for main core
	fwdn.exe -w %main-path%\ca72_bl3.rom --storage emmc --area user --part bl3_ca72_a
	echo.
	goto choose

:bootloader_sub
	echo.
	echo Boot Loader install for sub core
	fwdn.exe -w %sub-path%\ca53_bl3.rom --storage emmc --area user --part bl3_ca53_a 
	echo.
	goto choose

:kernel
	echo.
	echo Kernel install for main core
	fwdn.exe -w %main-path%\tc-boot-tcc8050-main.img --storage emmc --area user --part boot
	echo.
	goto choose

:kernel_sub
	echo.
	echo Kernel install for sub core
	fwdn.exe -w %sub-path%\tc-boot-tcc8050-sub.img --storage emmc --area user --part subcore_boot
	echo.
	goto choose

:dtb
	echo.
	echo DTB install for main core
	fwdn.exe -w %main-path%\tcc8050-linux-ivi-tost_sv0.1.dtb --storage emmc --area user --part dtb
	echo.
	goto choose

:dtb_sub
	echo.
	echo DTB install for sub core
	fwdn.exe -w %sub-path%\tcc8050-linux-subcore-ivi-tost_sv0.1.dtb --storage emmc --area user --part subcore_dtb
	echo.
	goto choose

:filesystem
	echo.
	echo File System install for main core
	fwdn.exe -w %main-path%\automotive-linux-platform-image-tcc8050-main.ext4 --storage emmc --area user --part system
	echo.
	goto choose

:filesystem_sub
	echo.
	echo File System install for sub core
	fwdn.exe -w %sub-path%\telechips-subcore-image-tcc8050-sub.ext4 --storage emmc --area user --part subcore_root
	echo.
	goto choose

:home
	echo.
	echo Home install for main core
	fwdn.exe -w deploy-images\home-directory.ext4 --storage emmc --area user --part home
	echo.
	goto choose

:home_sub
	echo.
	echo Home install for sub core
	if exist %deploy-images\home-directory.ext4 (		
		fwdn.exe -w deploy-images\home-directory.ext4 --storage emmc --area user --part home
		echo.
	)else (
		echo Not exist home-directory.ext4
	)	
	goto choose

:ubuntu
	echo.
	if not "%2" == "" (
		echo Ubuntu File System install for main core
		
		if exist %deploy-images\boot-firmware (
			echo Connect FWDN V8 to Board
			fwdn.exe --fwdn deploy-images\boot-firmware\fwdn.json
			fwdn.exe -w %2 --storage emmc --area user --part system
		)
	) else (
		echo Insert the ubuntu filesystem path.
	)
	exit /b

:ubuntu_main
	echo.
	echo Ubuntu File System install for main core
	fwdn.exe -w %main-path%\ubuntu-linux-platform-image-tcc8050-main.ext4 --storage emmc --area user --part system
	echo.
	goto choose

:help
	echo.
	echo Invalid Command
	echo.
	goto choose

:QUIT
	echo End !!