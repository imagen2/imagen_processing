#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


options = (
    (
        "validated_directory",
        {
            "type": "string",
            "default": "",
            "help": ("base directory in which the validated files"
                     " are copy from upload_directory."),
            "group": "imagen_upload", "level": 0,
        }
    ),
)
