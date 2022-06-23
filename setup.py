import cx_Freeze
executables = [cx_Freeze.Executable(script="spaceInvaders.py",icon="assets/spaceShip.ico")]
cx_Freeze.setup(
    name="Space Invaders",
    options={"build_exe": {"packages":["pygame"],
    "include_files":["assets"]}},
    executables = executables
 ) 