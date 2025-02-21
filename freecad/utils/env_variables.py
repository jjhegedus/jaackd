import os

def set_env_variable(var_name, var_value):
    home = os.path.expanduser("~")
    bashrc_path = os.path.join(home, ".bashrc")
    print(f"Setting environment variable {var_name} to {var_value} in {bashrc_path}")

    with open(bashrc_path, "a") as bashrc:
        bashrc.write(f"\nexport {var_name}={var_value}\n")

    print(f"Environment variable {var_name} set to {var_value} in {bashrc_path}")

def get_env_variable(var_name):
    return os.getenv(var_name)

def get_env_variables(grepStr):
    home = os.path.expanduser("~")
    bashrc_path = os.path.join(home, ".bashrc")

    with open(bashrc_path, "r") as bashrc:
        lines = bashrc.readlines()

    matching_vars = [line.strip() for line in lines if grepStr in line and line.startswith("export")]
    return matching_vars

# Example usage
# set_env_variable("MY_ENV_VAR", "my_value")
# print(get_env_variable("MY_ENV_VAR"))