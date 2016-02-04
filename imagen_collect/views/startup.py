#startup view

# CW imports
from cubicweb.web.views.startup import IndexView

# Cubes import
from cubes.piws.views.startup import NSIndexView


class IMAGENIndexView(IndexView):
    """ Class that defines the piws index view.
    """

    def call(self, **kwargs):
        """ Create the 'index' like page of our site.
        """
        # Get the card that contains some text description about this site
        self.w(u"THIS IS THE INDEX VIEW")

def registration_callback(vreg):
    vreg.register_and_replace(IMAGENIndexView, NSIndexView)
