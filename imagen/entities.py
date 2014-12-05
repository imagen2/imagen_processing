# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-imagen entity's classes"""

from cubicweb.selectors import is_instance
from cubicweb.view import EntityAdapter
from cubicweb.entities import AnyEntity, fetch_config


##############################################################################
# Define entities properties
##############################################################################

class Scan(AnyEntity):
    __regid__ = "Scan"

    def dc_title(self):
        """ Method the defined the scan entity title
        """
        dtype = self.r_has_data[0]
        return "{0} ({1})".format(self.label, dtype.__class__.__name__)

    @property
    def symbol(self):
        """ This property will return a symbol cooresponding to the scan
        type
        """
        dtype = self.r_has_data[0]
        if dtype.__class__.__name__ == "DMRIData":
            return "images/dmri.png"
        elif dtype.__class__.__name__ == "FMRIData":
            return "images/fmri.jpg"
        elif dtype.__class__.__name__ == "MRIData":
            return "images/mri.jpg"
        else:
            return "images/processing.png"


class Subject(AnyEntity):
    __regid__ = "Subject"

    def dc_title(self):
        """ Method the defined the subject entity title
        """
        return "{0}".format(self.code_in_study)

    @property
    def symbol(self):
        """ This property will return a symbol cooresponding to the subject
        gender
        """
        if self.gender == "male":
            return "images/male.png"
        elif self.gender == "female":
            return "images/female.png"
        else:
            return "images/unknown.png"


class QuestionnaireRun(AnyEntity):
    __regid__ = "QuestionnaireRun"

    def dc_title(self):
        """ Method the defined the questionnaire run entity title
        """
        subject = self.r_concerns[0]
        questionnaire = self.r_instance_of[0]
        assessment = self.reverse_uses[0]
        return "{0} - {1} - {2}".format(
            subject.code_in_study, questionnaire.name, assessment.timepoint)

    @property
    def symbol(self):
        """ This property will return a symbol cooresponding to the questionnaire
        run type
        """
        return "images/questionnaire.png"


class Assessment(AnyEntity):
    __regid__ = "Assessment"

    def dc_title(self):
        """ Method the defined the assessment entity title
        """
        subject = self.reverse_concerned_by[0]
        return "{0}".format(subject.code_in_study)

    @property
    def symbol(self):
        """ This property will return a symbol cooresponding to the scan
        type
        """
        return "images/samples.png"




class ScoreValue(AnyEntity):
    __regid__ = 'ScoreValue'

    def dc_title(self):
        return self.text

    @property
    def symbol(self):
        return '&#x261B;'

class ExternalResource(AnyEntity):
    __regid__ = 'ExternalResource'

    def dc_title(self):
        return self.name

    @property
    def symbol(self):
        return '&#x261B;'

class OpenAnswer(AnyEntity):
    __regid__ = 'OpenAnswer'

    def dc_title(self):
        return self.value

    @property
    def symbol(self):
        return '&#x261B;'

class Question(AnyEntity):
    __regid__ = 'Question'

    def dc_title(self):
        return self.text

    @property
    def symbol(self):
        return '&#x261B;'

class FMRIData(AnyEntity):
    __regid__ = 'FMRIData'

    def dc_title(self):
        return self.__class__.__name__

class DMRIData(AnyEntity):
    __regid__ = 'DMRIData'

    def dc_title(self):
        return self.__class__.__name__

class FMRIData(AnyEntity):
    __regid__ = 'FMRIData'

    def dc_title(self):
        return self.__class__.__name__

class MRIData(AnyEntity):
    __regid__ = 'MRIData'

    def dc_title(self):
        return self.__class__.__name__

class PROCESSINGData(AnyEntity):
    __regid__ = 'PROCESSINGData'

    def dc_title(self):
        return self.__class__.__name__


class GenomicMeasure(AnyEntity):
    __regid__ = 'GenomicMeasure'

    def dc_title(self):
        return self.chromset

    @property
    def symbol(self):
        return "48x48/genetics.png"
