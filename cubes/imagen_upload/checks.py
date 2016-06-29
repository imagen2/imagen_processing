# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

import os
import re
import shutil
import traceback

from imagen.sanity import cantab, imaging

SID_ERROR_MESSAGE = ("- The subject ID is malformed."
                     " [12 decimal digits required]<br/>")

UPLOAD_ALREADY_EXISTS = ("- A similar upload already exists."
                         " [Same subject ID and not rejected upload]."
                         " Please contact an administrator if you want"
                         " to force the upload.<br/>")

SYSTEM_ERROR_RAISED = ("- A system error raised."
                       " Please send the following message"
                       " to an administrator.")


def is_PSC1(upload):
    """ Cheks if sid field value is well formated (12 decimal digits)

    Pameters:
        upload: A CWUpload object

    Return:cubes/imagen/views/components.py
        Return True value match with the pattern, False otherwise
    """

    sid = upload.get_field_value('sid')
    if re.match("^\d{12}$", sid) is None:
        return False
    else:
        return True


def is_aldready_uploaded(upload):
    """ Cheks if an equivalent upload is already done.
        To be equivalent an upload must have:
            a status different than 'Rejected' and
            a uploadfield with equal SID

    Pameters:
        upload: A CWUpload object

    Return:
        Return True if an equivalent upload is already done, False otherwise
    """
    rql = ("Any COUNT(X) WHERE X is CWUpload,"
           " NOT X eid '{}',"
           " X form_name ILIKE '{}',"
           " NOT X status 'Rejected',"
           " X upload_fields F,"
           " F name 'sid',"
           " F value '{}'")
    rql = rql.format(
        upload.eid,
        upload.form_name,
        upload.get_field_value('sid'))
    rset = upload._cw.execute(rql)
    if rset.rows[0][0] == 0L:
        return False
    else:
        return True


def synchrone_check_cantab(upload):
    error = ''
    # checks
    if not is_PSC1(upload):
        error += SID_ERROR_MESSAGE
    if is_aldready_uploaded(upload):
        error += UPLOAD_ALREADY_EXISTS
    #dimitri check
    files = []
    for eUFile in upload.upload_files:
        files.append(eUFile.get_file_path())
    psc1, errors = cantab.check(files)
    if not psc1:
        for err in errors:
            error += err.__str__()

    # return
    if error:
        return (False, error)
    else:
        return (True, None)


def asynchrone_check_cantab(repository):
    """ Copy uploaded cantab files from 'upload_dir' to 'validated_dir/...'
        and set status 'validated'
    """
    validated_dir = repository.vreg.config["validated_directory"]
    rql = ("Any X WHERE X is CWUpload,"
           " X form_name ILIKE 'cantab', X status 'Quarantine'")
    with repository.internal_cnx() as cnx:
        rset = cnx.execute(rql)
        for entity in rset.entities():
            for eUFile in entity.upload_files:
                from_file = eUFile.get_file_path()
                to_file = u'{0}/{1}/{2}'.format(
                    validated_dir,
                    entity.get_field_value('centre'),
                    entity.get_field_value('sid')
                )
                if not os.path.exists(to_file):
                    os.makedirs(to_file)
                to_file = to_file + "/{}".format(eUFile.data_name)
                shutil.copy2(from_file, to_file)
            rql = ("SET X status 'Validated'"
                   " WHERE X is CWUpload, X eid '{}'".format(entity.eid))
            cnx.execute(rql)
        cnx.commit()


def synchrone_check_image(upload):
    error = ''
    # checks
    if not is_PSC1(upload):
        error += SID_ERROR_MESSAGE
    if is_aldready_uploaded(upload):
        error += UPLOAD_ALREADY_EXISTS
    #dimitri check
    psc1, errors = imaging.check(upload.upload_files[0].get_file_path())
    if not psc1:
        for err in errors:
            error += err.__str__()
    # return
    if error:
        return (False, error)
    else:
        return (True, None)


def asynchrone_check_image(repository):

    validated_dir = repository.vreg.config["validated_directory"]
    rql = ("Any X WHERE X is CWUpload,"
           " X form_name ILIKE 'image', X status 'Quarantine'")
    with repository.internal_cnx() as cnx:
        rset = cnx.execute(rql)
        for entity in rset.entities():
            try:
                psc1, errors = imaging.extended_check(
                    entity.upload_files[0].get_file_path())
                error = ''
                if not psc1:
                    for err in errors:
                        error += err.__str__()
                    rql = ("SET X status 'Rejected', X error '{}'"
                           " WHERE X is CWUpload, X eid {}".format(
                               error, entity.eid))
                else:
                    from_file = entity.upload_files[0].get_file_path()
                    to_file = u'{0}/{1}/{2}'.format(
                        validated_dir,
                        entity.get_field_value('centre'),
                        entity.get_field_value('sid')
                    )
                    if not os.path.exists(to_file):
                        os.makedirs(to_file)
                    to_file = to_file + "/{}".format(
                        entity.upload_files[0].data_name)
                    shutil.copy2(from_file, to_file)
                    rql = ("SET X status 'Validated'"
                           " WHERE X is CWUpload, X eid '{}'".format(
                               entity.eid))
                cnx.execute(rql)
            except:
                stacktrace = traceback.format_exc()
                stacktrace = stacktrace.replace('"', "'").replace("'", "\\'")
                rql = ("SET X status 'Rejected', X error '{} <br/> {}'"
                       " WHERE X is CWUpload, X eid '{}'".format(
                           SYSTEM_ERROR_RAISED,
                           stacktrace,
                           entity.eid))
                cnx.execute(rql)
        cnx.commit()
