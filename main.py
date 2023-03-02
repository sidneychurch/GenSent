
# For Pyinstalller to work:
#   - use auto-py-to-exe
#   - Options:
#       - One File
#       - Window Based
#       - Additional Files:
#           - Lib/site-packages/pronouncing
#           - Lib/site-packages/cmudict
#           - icon file
#       - Advanced:
#           - collect-all:
#               - pronouncing
#               - cmudict
#           - copy-metadata:
#               - cmudict

import GUI


GUI.launch_GUI()
