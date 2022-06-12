from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        
        response = {
          "code": renderer_context['response'].status_code,
          "message": renderer_context['response'].status_text,
          "data": data
        }
        
        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
