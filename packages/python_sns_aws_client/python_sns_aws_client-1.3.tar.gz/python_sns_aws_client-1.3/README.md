******Python SNS Client******

1.- Install pip

2.- Add credentials to env
    
    AWS_ACCESS_KEY_ID = 'AWS_KEY'
    AWS_SECRET_ACCESS_KEY = 'AWS_SECRET'
    AWS_DEFAULT_REGION = 'us-west-2"' 
    
Usage


1.- Add your routes

    Example Django
    
    from sns.view import PushView, SNSView

    urlpatterns = [
        url(r'^push', PushView.as_view()),
        url(r'^sns', SNSView.as_view()),
    ]
    
    Example Flask
    
    @app.route('/sns', methods=['POST'])
    def sns_topic():
    
    @app.route('/publish', methods=['POST'])
    def sns_publish():
    
2.- Add view or function listen
    
    Example Django
    
    @method_decorator(csrf_exempt, name='dispatch')
    class SnsBaseView(generic.TemplateView):
        template_name = 'snsclient.html'
    
        def post(self, request, *args, **kwargs):
            context = self.get_context_data(*args, **kwargs)
            return self.render_to_response(context)
        
    class SNSView(SnsBaseView):
    
        def post(self,request,*args,**kwargs):
            Client.validator(request.body)
            return super().post(request, *args, **kwargs)
    
    Example Flask
    @app.route('/sns', methods=['POST'])
    def sns_topic():
        if request.method == 'POST':
            client = Client.validator(request.data)
            return 'SNS-TOPIC!! {}'.format(client)

3.- Push your message to SNS

    Example Django   
    
    from sns.utils import Client
    
    class PushView(SnsBaseView):

        def post(self, request, *args, **kwargs):
            publish = {
                'subject': request.POST.get('subject'),
                'message': request.POST.get('message')
            }
            cli = Client()
            cli.publish(**publish)
            return super().post(request, *args, **kwargs) 
    
    Example Flask
    
    @app.route('/publish', methods=['POST'])
    def sns_publish():
        if request.method == 'POST':
            publish = {
                'subject': request.form['subject'],
                'message': request.form['message']
            }
            cli = Client()
            cli.publish(**publish)
            return 'PUBLISH-SNS-TOPIC!!'