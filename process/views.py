from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
                TemplateView,
                CreateView,
                DetailView,
                DeleteView,
                ListView,
                UpdateView,
                View,
                RedirectView,
                )
from django.views.generic.edit import FormMixin, FormView
from process.mixins import FormUserNeededMixin, UserOwnerMixin
from process.models import *
from process.forms import *
from process.include import *
from process.subject_topic_list import *
from process.subject_calculus_1 import *
from process.subject_simplemath import *
from process.subject_differential_equation import *



class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['data_of_home_page'] = HomePage.objects.first()
        context['subjecs'] = Subject.objects.all()
        context['streams'] = streams = Stream.objects.all()
        context['sessions'] = AssignmentSession.objects.all()
        if self.request.user.is_staff:
            context['assignments'] = Assignment.objects.all()
            context['streams'] = streams = Stream.objects.all()
        elif self.request.user.is_authenticated:
            context['assignments'] = Assignment.objects.all()
            context['streams'] = streams = Stream.objects.all()
        return context


class StreamListView(ListView):
    template_name = 'streams/streams.html'
    model = Stream
    context_object_name = 'streams'


class StreamDetailView(DetailView):
    template_name = 'streams/stream-detail.html'
    model = Stream
    context_object_name='stream'

    def get_context_data(self,**kwargs):
        context = super(StreamDetailView,self).get_context_data(**kwargs)
        enroll_form = StreamEnrollForm(self.request.GET or None)
        unenroll_form = StreamUnEnrollForm(self.request.GET or None)
        context['enroll_form'] = enroll_form
        context['unenroll_form'] = unenroll_form
        return context


class StreamEnrolelView(FormView):
    form_class = StreamEnrollForm
    model = Stream
    template_name = 'streams/stream-detail.html'
    # success_url = reverse_lazy('process:stream_detail')

    def form_valid(self, form):
        context = super(StreamEnrolelView, self).form_valid(form)
        stream_slug = self.kwargs['slug']
        stream  = Stream.objects.get(slug = stream_slug)
        enroll_key = stream.enroll_key
        user = self.request.user
        enrollment_key = form.cleaned_data['enrollment_key']
        if enroll_key == enrollment_key:
            stream.users.add(user)
            stream.save()
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('process:stream_detail', kwargs = {'slug': self.kwargs['slug']})


class StreamUnenrollView(FormView):
    form_class = StreamUnEnrollForm
    model = Stream
    template_name = 'streams/stream-detail.html'
    # success_url = reverse_lazy('process:stream_detail')

    def form_valid(self, form):
        stream_slug = self.kwargs['slug']
        stream  = Stream.objects.get(slug = stream_slug)
        user = self.request.user
        stream.users.remove(user)
        stream.save()
        return super(StreamUnenrollView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('process:stream_detail', kwargs = {'slug': self.kwargs['slug']})


class SubjectListView(ListView):
    template_name = 'subjects/subjects.html'
    model = Subject
    context_object_name = 'subjects'


class SubjectDetailView(DetailView):
    template_name = 'subjects/subject-detail.html'
    model = Subject
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super(SubjectDetailView, self).get_context_data(**kwargs)
        subject_id = kwargs['object'].id
        context['topics'] = Topic.objects.filter(subject_id = subject_id)
        return context


class TopicDetailView(DetailView):
    template_name = 'topics/topic-detail.html'
    model = Topic
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_context_data(self,**kwargs):
        context = super(TopicDetailView,self).get_context_data(**kwargs)
        topic_check = TopicTakeAnswerForm(self.request.GET or None)
        context['topic_check_context'] = topic_check
        topic_slug = kwargs['object'].slug
        topic_code = kwargs['object'].function_code
        question = question_creater(topic_code)
        context['topic_latex_question'] = latex(question)
        context['topic_question'] = question
        return context


class TopicCheckAnswerView(FormView):
    form_class = TopicTakeAnswerForm
    template_name = 'topics/topic-detail.html'
    model = Topic
    slug_url_kwarg = 'topic_slug'

    # def get_context_data(self, **kwargs):
    #     context = super(TopicDetailView, self).get_context_data(**kwargs)
        # topic_slug = kwargs['object'].slug
        # return context


    def form_valid(self, form):
        context = super(TopicCheckAnswerView, self).form_valid(form)
        topic_slug = self.kwargs['slug']
        topic  = Topic.objects.get(slug = topic_slug)
        topic_code = topic.function_code
        # user = self.request.user
        user_answer = form.cleaned_data['user_answer']
        topic_question = self.request.POST['question']
        # print(topic_question)
        # context['true_false_answer'] = questions_t_o_f(topic_code, topic_question, user_answer)
        context['answer'] = question_solver(topic_code, topic_question)
        # print(self.request.path)
        # print(context['true_false_answer'])
        print(context['answer'], "Answer")
        return super(TopicCheckAnswerView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('process:topic_detail', kwargs = {'slug': 'calculus-1','topic_slug': self.kwargs['slug']})


    # def get(self, request):
    #     form = TopicTakeAnswerForm()
    #     return render(request, self.template_name, {'form':form})
    #
    # def post(self, request):
    #     form = TopicTakeAnswerForm(request.POST)
    #     if form.is_valid():
    #         text = form.cleaned_data['post']
    #         form = TopicTakeAnswerForm()
    #         return redirect('process:topic_detail', kwargs = {'slug': 'simple-math','topic_slug': self.kwargs['slug']})
    #
    #     args = {'form': form, 'text': text}
    #     return render(request, self.template_name, args)

def check_user_answer(request):
    print('Check answer is work!')
    # subject = get_object_or_404(Subject, slug)
    # topic = get_object_or_404(Topic, slug = topic_slug)
    user_answer = request.GET.get('user_answer', None)
    topic_slug = [ i for i in request.GET.get('my_location', None).split('/')][4]
    topic_question = request.GET.get('topic_question', None)
    topic  = Topic.objects.get(slug = topic_slug)
    print(topic, 'This is Toic!')
    topic_code = topic.function_code
    print(topic_code, "This is topic code!")
    # user = self.request.user
    # true_false_answer = questions_t_o_f(topic_code, topic_question, user_answer)
    answer = question_solver(topic_code, topic_question)
    print(answer, 'Answer 1')
    answer = latex(answer)
    print(answer, 'Answer 2')
    context = {
        # 'true_false_answer': true_false_answer,
        'answer': answer,
    }
    return JsonResponse(context)

class AssignmentListView(ListView):
    template_name = 'assignments/assignment-list.html'
    model = Assignment
    context_object_name = 'assignments'


class AssignmentDetailView(DetailView):
    template_name = 'assignments/assignment-form.html'
    model = Assignment
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        context = super(AssignmentDetailView,self).get_context_data(**kwargs)
        assignment_slug = self.kwargs['slug']
        user = self.request.user

        try:
            assignment = Assignment.objects.get(slug=assignment_slug)
            stream = assignment.stream
        except Assignment.DoesNotExist:
            messages.add_message(self.request, messages.WARNING, "Assignment " + assignment_slug + " does not exist")
            raise Http404("Assignment " + assingment + " does not exist")

        if user not in stream.users.all() or user.is_staff:
            messages.add_message(self.request, messages.WARNING, 'This assignment is not available for you')
            raise Http404("This assignment is not available for you")

        try:
            assignment_session = AssignmentSession.objects.get(user=user, assignment=assignment)


        except AssignmentSession.DoesNotExist:
            if assignment.available_from > timezone.now():
                messages.add_message(self.request, messages.WARNING, 'This assignment is not available yet')
                raise Http404('This assignment is not available yet')
                # return redirect('process:index')
                # return HttpResponseRedirect(reverse('process:assignment_list'))

            assignment_session = AssignmentSession.objects.create_session(user, assignment)
            assignment_session_question = AssignmentSessionQuestions.objects.create_session_question(assignment_session, assignment)

        question_index = assignment_session.current_index
        question_count = assignment_session.questions_amount
        assignment_end = assignment.available_from + datetime.timedelta(minutes=assignment.available_for_x_minutes)

        if question_index >= question_count:
            assignment_session.current_index = question_count
            assignment_session.save()
            messages.add_message(self.request, messages.INFO, 'This assignment you already finished!')

            raise Http404('This assignment you already finished!')
            # return redirect('process:index')
            # return HttpResponseRedirect(reverse('process:assignment_list'))

        # question_id = int(assignment_session.questions_amount.split(",")[question_index])
        question_list = AssignmentSessionQuestions.objects.filter(session = assignment_session)
        question_id_list = [ q_id.id for q_id in question_list ]

        context['assignment_end'] = assignment_end
        context['question'] = AssignmentSessionQuestions.objects.get(id = question_id_list[question_index])
        context['progress'] = ProgressBar(question_index, question_count)
        context['form'] = AssignmentFormViewForm(self.request.GET or None)
        return context

    # def render_to_response(self, context):
    #     try:
    #         assignment = Assignment.objects.get(slug=assignment_slug)
    #     except Assignment.DoesNotExist:
    #         return redirect('process:index')
    #
    #     try:
    #         assignment_session = AssignmentSession.objects.get(user=user, assignment=assignment)
    #     except AssignmentSession.DoesNotExist:
    #         return redirect('process:index')
    #
    #     if question_index >= question_count or timezone.now() > assingment_end:
    #         return redirect('process:index')
    #
    #     return super(AssignmentDetailView, self).render_to_response(context)

class AssignmentFormView(FormView):
    template_name = 'assignments/assignment-form.html'
    model = Assignment
    form_class = AssignmentFormViewForm
    context_object_name = 'assignment'


    def form_valid(self, form, **kwargs):
        context = super(AssignmentFormView,self).get_context_data(**kwargs)
        assignment_slug = self.kwargs['slug']
        print(assignment_slug)
        user = self.request.user
        try:
            assignment = get_object_or_404(Assignment, slug=assignment_slug)
        except Assignment.DoesNotExist:
            messages.add_message(self.request, messages.WARNING, "Assignment " + assignment_slug + " does not exist")
            raise Http404("Assignment " + assignment_slug + " does not exist")


        assignment_session = AssignmentSession.objects.get(assignment = assignment, user = user)
        question_index = assignment_session.current_index
        question_list = AssignmentSessionQuestions.objects.filter(session = assignment_session)
        question_id_list = [ q_id.id for q_id in question_list ]
        question_id = int(question_id_list[question_index])
        question = AssignmentSessionQuestions.objects.get(id=question_id)

        answer = form.cleaned_data['answer']
        question.user_answer = answer
        # questions_t_o_f() solve question and compare with user aswer and return True or False from givens
        question.is_correct = questions_t_o_f(question.topic.function_code, question.question, answer)
        # question_solver() solve question and return answers
        question.question_answer = question_solver(question.topic.function_code, question.question)
        question.finished_at =  timezone.now()
        question.save()


        assignment_session.current_index += 1
        if question.is_correct is True:
            assignment_session.correct_answers +=1
        elif question.is_correct is False:
            assignment_session.incorrect_answers +=1
        else:
            raise Http404('Erorr please contact to developer!!!')
        assignment_session.save()

            # return redirect('/assignments/%s/' % assignment_slug)
        return redirect('/assignments/%s/' % assignment_slug)

    def get_success_url(self, **kwargs):
        return reverse_lazy('process:assignment_seshion_final', kwargs = {'slug': self.kwargs['slug']})


class AssignmentSessionFinalView(DetailView):
    template_name = 'assignments/assignment-final.html'
    model = AssignmentSession
    context_object_name = 'result'


class AssignmentResultsListView(ListView):
    template_name = 'assignments/user-assignment-results-list.html'
    model = AssignmentSession
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super(AssignmentResultsListView,self).get_context_data(**kwargs)
        user_assignments = AssignmentSession.objects.filter(user = self.request.user)
        context['user_assignments'] = user_assignments
        return context

class AssignmentResultDetailView(DetailView):
    template_name = 'assignments/user-assignment-result-detail.html'
    model = AssignmentSession
    context_object_name = 'result'

    def get_context_data(self, **kwargs):
        context = super(AssignmentResultDetailView,self).get_context_data(**kwargs)
        context['questions'] = AssignmentSessionQuestions.objects.filter(session = kwargs['object'])
        return context

class CuratorAssignmentList(ListView):
    template_name = 'assignments/curator-assingment-list.html'
    model = Assignment
    context_object_name = 'supper_assignments'


class CuratorAssignmentSessionList(DetailView):
    template_name = 'assignments/curator-assingment-user-list.html'
    model = Assignment
    context_object_name = 'supper_assignments_session'

    def get_context_data(self, **kwargs):
        context = super(CuratorAssignmentSessionList,self).get_context_data(**kwargs)
        assignment_session_list = AssignmentSession.objects.filter(assignment = kwargs['object'])
        context['assignment_session_list'] = assignment_session_list
        return context


class CuratorAssignmentUserSessionResult(DetailView):
    template_name = 'assignments/curator-assignment-user-detail.html'
    model = AssignmentSession
    context_object_name = 'supper_sesion_result'

    def get_context_data(self, **kwargs):
        context = super(CuratorAssignmentUserSessionResult,self).get_context_data(**kwargs)
        context['questions'] = AssignmentSessionQuestions.objects.filter(session = kwargs['object'])
        return context
