# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

import hashlib
import os
import re
import shutil
import traceback

from cubes.rql_upload.tools import get_or_create_logger
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


def get_message_error(flag, errors):
    message = ''
    if not flag:
        for err in errors:
            message += err.__str__()
            message += u'<br/>'
    return message


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
    message = ''
    # checks
    if not is_PSC1(upload):
        message += SID_ERROR_MESSAGE
    if is_aldready_uploaded(upload):
        message += UPLOAD_ALREADY_EXISTS

    #dimitri check
    sid = upload.get_field_value('sid')
    tid = upload.get_field_value('time_point')
    for ufile in upload.upload_files:
        psc1 = True
        errors = None
        if ufile.name == 'cant':
            psc1, errors = cantab.check_cant_name(ufile.data_name, sid, tid)
            message += get_message_error(psc1, errors)
            psc1, errors = cantab.check_cant_content(
                ufile.get_file_path(), sid, tid)
            message += get_message_error(psc1, errors)
        elif ufile.name == 'datasheet':
            psc1, errors = cantab.check_datasheet_name(
                ufile.data_name, sid, tid)
            message += get_message_error(psc1, errors)
            psc1, errors = cantab.check_datasheet_content(
                ufile.get_file_path(), sid, tid)
            message += get_message_error(psc1, errors)
        elif ufile.name == 'detailed_datasheet':
            psc1, errors = cantab.check_detailed_datasheet_name(
                ufile.data_name, sid, tid)
            message += get_message_error(psc1, errors)
            psc1, errors = cantab.check_detailed_datasheet_content(
                ufile.get_file_path(), sid, tid)
            message += get_message_error(psc1, errors)
        elif ufile.name == 'report':
            psc1, errors = cantab.check_report_name(ufile.data_name, sid, tid)
            message += get_message_error(psc1, errors)
            psc1, errors = cantab.check_report_content(
                ufile.get_file_path(), sid, tid)
            message += get_message_error(psc1, errors)

    # return
    if message:
        return (False, message)
    else:
        return (True, None)


def asynchrone_check_cantab(repository):
    """ Copy uploaded cantab files from 'upload_dir' to 'validated_dir/...'
        and set status 'validated'
    """

    logger = get_or_create_logger(repository.vreg.config)
    validated_dir = repository.vreg.config["validated_directory"]

    rql = ("Any X WHERE X is CWUpload,"
           " X form_name ILIKE 'cantab', X status 'Quarantine'")
    with repository.internal_cnx() as cnx:
        rset = cnx.execute(rql)
        for entity in rset.entities():
            try:
                sid = entity.get_field_value('sid')
                centre = entity.get_field_value('centre')
                tp = entity.get_field_value('time_point')
                for eUFile in entity.upload_files:
                    from_file = eUFile.get_file_path()
                    to_file = u'{0}/{1}/{2}/{3}'.format(
                        validated_dir, tp, centre, sid)
                    if not os.path.exists(to_file):
                        os.makedirs(to_file)
                    to_file = to_file + "/{}".format(eUFile.data_name)
                    shutil.copy2(from_file, to_file)
                    sha1 = unicode(
                        hashlib.sha1(open(to_file, 'rb').read()).hexdigest())
                    if sha1 == eUFile.data_sha1hex:
                        os.remove(from_file)
                        os.symlink(to_file, from_file)
                        logger.info(
                            ("Copy from '{}' to '{}'"
                             ", delete and create symlink".format(
                                 from_file, to_file)))
                    else:
                        logger.critical(
                            "Incorrect copy from '{}' to '{}'".format(
                                from_file, to_file))
                rql = ("SET X status 'Validated'"
                       " WHERE X is CWUpload, X eid '{}'".format(entity.eid))
                cnx.execute(rql)
            except:
                stacktrace = traceback.format_exc()
                stacktrace = stacktrace.replace('"', "'").replace("'", "\\'")
                logger.critical("A system error raised")
                rql = ("SET X status 'Rejected', X error '{} <br/> {}'"
                       " WHERE X is CWUpload, X eid '{}'".format(
                           SYSTEM_ERROR_RAISED,
                           stacktrace,
                           entity.eid))
                cnx.execute(rql)

        cnx.commit()


def synchrone_check_rmi(upload):
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
            error += u'<br/>'
    # return
    if error:
        return (False, error)
    else:
        return (True, None)


def asynchrone_check_rmi(repository):

    logger = get_or_create_logger(repository.vreg.config)
    validated_dir = repository.vreg.config["validated_directory"]
    rql = ("Any X WHERE X is CWUpload,"
           " X form_name ILIKE 'MRI', X status 'Quarantine'")
    with repository.internal_cnx() as cnx:
        rset = cnx.execute(rql)
        for entity in rset.entities():
            sid = entity.get_field_value('sid')
            centre = entity.get_field_value('centre')
            tp = entity.get_field_value('time_point')
            try:
                psc1, errors = imaging.extended_check(
                    entity.upload_files[0].get_file_path())
                error = ''
                if not psc1:
                    for err in errors:
                        error += err.__str__()
                        error += u'<br/>'
                    rql = ("SET X status 'Rejected', X error '{}'"
                           " WHERE X is CWUpload, X eid {}".format(
                               error, entity.eid))
                else:
                    from_file = entity.upload_files[0].get_file_path()
                    to_file = u'{0}/{1}/{2}/{3}'.format(
                        validated_dir, tp, centre, sid)
                    if not os.path.exists(to_file):
                        os.makedirs(to_file)
                    to_file = to_file + "/{}".format(
                        entity.upload_files[0].data_name)
                    shutil.copy2(from_file, to_file)
                    sha1 = unicode(
                        hashlib.sha1(open(to_file, 'rb').read()).hexdigest())
                    if sha1 == entity.upload_files[0].data_sha1hex:
                        os.remove(from_file)
                        os.symlink(to_file, from_file)
                        logger.info(
                            ("Copy from '{}' to '{}'"
                             ", delete and create symlink".format(
                                 from_file, to_file)))
                    else:
                        logger.critical(
                            "Incorrect copy from '{}' to '{}'".format(
                                from_file, to_file))
                    rql = ("SET X status 'Validated'"
                           " WHERE X is CWUpload, X eid '{}'".format(
                               entity.eid))
                cnx.execute(rql)
            except:
                stacktrace = traceback.format_exc()
                stacktrace = stacktrace.replace('"', "'").replace("'", "\\'")
                logger.critical("A system error raised")
                rql = ("SET X status 'Rejected', X error '{} <br/> {}'"
                       " WHERE X is CWUpload, X eid '{}'".format(
                           SYSTEM_ERROR_RAISED,
                           stacktrace,
                           entity.eid))
                cnx.execute(rql)
        cnx.commit()
