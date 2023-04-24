from eddai_EliteDangerousApiInterface.settings.default import INSTALLED_APPS, BASE_DIR
from core.router import EDInfoRouter

import os 
import sys


route_app_labels = EDInfoRouter.route_app_labels
env_path = BASE_DIR.parent / "venv" / "Scripts"


def main():

    param = sys.argv

    setting = param[param.index("--settings")+1]

    operating_system = os.name

    os.system(f"source {env_path / 'activate'}")

    for app in INSTALLED_APPS:
        if app in  route_app_labels:
            os.system(f"python {BASE_DIR / 'manage.py'} migrate {app} --database ed_info --setting {setting}")
        else:
            os.system(f"python {BASE_DIR / 'manage.py'} migrate {app} --database default --setting {setting}")

if __name__=="__main__":
    main()