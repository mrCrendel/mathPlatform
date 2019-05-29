from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
                TemplateView,
                CreateView,
                DetailView,
                DeleteView,
                ListView,
                UpdateView,
                View,
                RedirectView
                )
from django.views.generic.edit import FormView
from process.models import *
from process.forms import *
from process.include import *
from process.mixins import FormUserNeededMixin, UserOwnerMixin
# from process.math.math_differential_equation import *


class IndexTemplateView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        context = super(IndexTemplateView, self).get_context_data(**kwargs)

        print(self.request.user)
        context['data_of_home_page'] = HomePage.objects.first()
        context['subjects'] = Subject.objects.all()
        context['streams'] = Stream.objects.all()
        context['sessions'] = AssignmentSession.objects.all()
        if self.request.user.is_staff:
            context['assignments'] = Assignment.objects.filter(user=self.request.user)
        elif self.request.user.is_authenticated:
            context['assignments'] = Assignment.objects.filter(stream__users=self.request.user).filter(active=True)
        return context


class StreamListView(ListView):
    template_name = 'streams/streams.html'
    model = Stream
    context_object_name = 'streams'


class StreamDetailView(DetailView):
    template_name = 'streams/stream-detail.html'
    model = Stream
    context_object_name = 'stream'

    def get_context_data(self, **kwargs):
        context = super(StreamDetailView, self).get_context_data(**kwargs)
        enroll_form = StreamEnrollForm(self.request.GET or None)
        unenroll_form = StreamUnEnrollForm(self.request.GET or None)
        context['enroll_form'] = enroll_form
        context['unenroll_form'] = unenroll_form
        return context


class StreamCreateView(SuccessMessageMixin, FormUserNeededMixin, CreateView):
    form_class = StreamFormCreate
    template_name = 'streams/curator-stream-form-create.html'
    success_url = reverse_lazy('/')
    success_message = "%(suc_message)s"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           suc_message="Stream {0} successfully created".format(self.object.title))


class StreamUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserOwnerMixin, UpdateView, RedirectView):
    form_class = StreamFormUpdate
    model = Stream
    template_name = 'streams/curator-stream-form-update.html'
    context_object_name = 'update_stream'
    # success_url = reverse_lazy('process:index')
    success_message = "%(suc_message)s"

    def get_context_data(self, **kwargs):
        context = super(StreamUpdateView, self).get_context_data(**kwargs)
        context['delete_url'] = '/streams/{0}/delete/'.format(self.object.slug)
        return context

    # def get_redirect_url(self, *args, **kwargs):
    #     slug = self.kwargs.get("slug")
    #     obj = get_object_or_404(Store, slug=slug)
    #     url_ = obj.get_absolute_url()
    #     # self.request.user
    #     return url_

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           suc_message="Stream {0} successfully updated ".format(self.object.title))


class StreamDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """
    form_class = StreamFormCreate
    model = Stream
    # success_url = reverse_lazy('webapp:stores')
    template_name = 'streams/curator-stream-form-create.html'
    success_message = "Stream successfully deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(StreamDeleteView, self).delete(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           suc_message="Stream {0} successfully deleted".format(self.object.title))


class StreamEnrolelView(FormView):
    form_class = StreamEnrollForm
    model = Stream
    template_name = 'streams/stream-detail.html'
    # success_url = reverse_lazy('process:stream_detail')

    def form_valid(self, form):
        context = super(StreamEnrolelView, self).form_valid(form)
        stream_slug = self.kwargs['slug']
        stream = Stream.objects.get(slug=stream_slug)
        enroll_key = stream.enroll_key
        user = self.request.user
        enrollment_key = form.cleaned_data['enrollment_key']
        if enroll_key == enrollment_key:
            stream.users.add(user)
            stream.save()
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('process:stream_detail', kwargs={'slug': self.kwargs['slug']})


class StreamUnenrollView(FormView):
    form_class = StreamUnEnrollForm
    model = Stream
    template_name = 'streams/stream-detail.html'
    # success_url = reverse_lazy('process:stream_detail')

    def form_valid(self, form):
        stream_slug = self.kwargs['slug']
        stream = Stream.objects.get(slug=stream_slug)
        user = self.request.user
        stream.users.remove(user)
        stream.save()
        return super(StreamUnenrollView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy('process:stream_detail', kwargs={'slug': self.kwargs['slug']})


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
        context['topics'] = Topic.objects.filter(subject_id=subject_id)
        return context


class TopicDetailView(DetailView):
    template_name = 'topics/topic-detail.html'
    model = Topic
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        topic_check = TopicTakeAnswerForm(self.request.GET or None)


        context['topic_check_context'] = topic_check
        topic_slug = kwargs['object'].slug
        function_code = kwargs['object'].function_code
        question = question_creater(function_code)
        # print(latex(question))
        context['topic_latex_question'] = latex(question)
        context['topic_description'] = kwargs['object'].description
        if TopicList.is_differential_equation_with(function_code):
            # print(question[0])
            print(type(kwargs['object'].description))
            context['topic_description'] = (kwargs['object'].description).format(question[1], question[2])
            # print(context['topic_description'])
            context['topic_latex_question'] = latex(question[0])
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
        topic = Topic.objects.get(slug=topic_slug)
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
        return reverse_lazy('process:topic_detail', kwargs={'slug': 'calculus-1', 'topic_slug': self.kwargs['slug']})


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
    user_answer = request.GET.get('user_answer', None)
    topic_slug = [i for i in request.GET.get('my_location', None).split('/')][4]
    topic_question = request.GET.get('topic_question', None)
    topic = Topic.objects.get(slug=topic_slug)
    topic_code = topic.function_code
    true_false_answer = questions_t_o_f(topic_code, topic_question, user_answer)
    print(true_false_answer)
    print(type(true_false_answer))
    answer1 = question_solver(topic_code, topic_question)
    print(type(answer1), 'Answer 1')
    answer = latex(answer1)
    context = {
        'true_false_answer': true_false_answer,
        # 'answer1': answer1,
        'answer': answer,
    }
    return JsonResponse(context)


def window_looses_foxus(request):
    question_topic = request.GET.get('question_topic', None)
    question_id = request.GET.get('question_id', None)
    topic = Topic.objects.get(title=question_topic)
    # print('id', question_id)
    topic_fuction_code = topic.function_code
    new_question = question_creater(topic_fuction_code)
    session_question = get_object_or_404(AssignmentSessionQuestions, id=question_id)
    session_question.question = new_question
    new_description = topic.description
    if TopicList.is_differential_equation_with(topic_fuction_code):
        session_question.description = (topic.description).format(new_question[1], new_question[2])
        new_description = (topic.description).format(new_question[1], new_question[2])
        new_question = new_question[0]

    session_question.save()
    context = {
        'new_description': new_description,
        'new_question': str(latex(new_question)),
    }
    return JsonResponse(context)


def load_topics(request):
    subject_id = request.GET.get('subject')
    subject = get_object_or_404(Subject, id=subject_id)
    topics = Topic.objects.filter(subject=subject)
    # context = {
    #     {'topic': topic}
    # }
    # return JsonResponse(context)
    return render(request, 'includes/city_dropdown_list_options.html', {'topics': topics})


class AssignmentCreateView(SuccessMessageMixin, FormUserNeededMixin, CreateView):
    model = Assignment
    form_class = AssignmentCreateForm
    template_name = 'assignments/curator-assignment-create.html'
    success_url = reverse_lazy('process:index')
    success_message = "%(suc_message)s"

    # def get_context_data(self, **kwargs):
    #     context = super(AssignmentCreateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['topic_formset'] = AssignmentTopicFormSet(self.request.POST)
    #     else:
    #         context['topic_formset'] = AssignmentTopicFormSet()
    #     return context
    #
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context['topic_formset']
    #     if formset.is_valid():
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return redirect(self.success_url)
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(AssignmentCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['addtopic'] = AssignmentTopicFormSet(data=self.request.POST, files=self.request.FILES,
                                                         instance=self.object)
        else:
            context['addtopic'] = AssignmentTopicFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        addgallery = context['addtopic']

        with transaction.atomic():
            self.object = form.save()

            if addgallery.is_valid():
                addgallery.instance = self.object
                addgallery.save()
        return super(AssignmentCreateView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           suc_message="Assignment {0} successfully created".format(self.object.title))


class AssignmentUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserOwnerMixin, UpdateView, RedirectView):
    form_class = AssignmentCreateForm
    model = Assignment
    template_name = 'assignments/curator-assignment-update.html'
    context_object_name = 'update_stream'
    success_url = reverse_lazy('process:index')
    success_message = "%(suc_message)s"

    def get_context_data(self, **kwargs):
        context = super(AssignmentUpdateView, self).get_context_data(**kwargs)
        context['delete_url'] = '/assignments/{0}/delete/'.format(self.object.slug)
        if self.request.POST:
            context['addtopic'] = AssignmentTopicFormSet(data=self.request.POST, files=self.request.FILES,
                                                         instance=self.object)
        else:
            context['addtopic'] = AssignmentTopicFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        addgallery = context['addtopic']

        with transaction.atomic():
            self.object = form.save()

            if addgallery.is_valid():
                addgallery.instance = self.object
                addgallery.save()
        return super(AssignmentUpdateView, self).form_valid(form)
    # def get_context_data(self, **kwargs):
    #     context = super(AssignmentUpdateView, self).get_context_data(**kwargs)
    #     context['delete_url'] = '/assignments/{0}/delete/'.format(self.object.slug)
    #     if self.request.POST:
    #         context['track_formset'] = AssignmentTopicFormSet(self.request.POST, instance=self.object)
    #         context['topic_formset'].full_clean()
    #     else:
    #         context['topic_formset'] = AssignmentTopicFormSet(instance=self.object)
    #     return context
    #
    # def form_valid(self, form):
    #     context = self.get_context_data()
    #     formset = context['topic_formset']
    #     if formset.is_valid():
    #         self.object = form.save()
    #         formset.instance = self.object
    #         formset.save()
    #         return redirect(self.success_url)
    #     else:
    #         return self.render_to_response(self.get_context_data(form=form))

    # def get_context_data(self, **kwargs):
    #     context = super(AssignmentUpdateView, self).get_context_data(**kwargs)
    #     context['delete_url'] = '/assignments/{0}/delete/'.format(self.object.slug)
    #     return context

    # def get_redirect_url(self, *args, **kwargs):
    #     slug = self.kwargs.get("slug")
    #     obj = get_object_or_404(Store, slug=slug)
    #     url_ = obj.get_absolute_url()
    #     # self.request.user
    #     return url_

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           suc_message="Assignment {0} successfully updated ".format(self.object.title))


class AssignmentDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """
    form_class = AssignmentCreateForm
    model = Assignment
    success_url = reverse_lazy('process:index')
    template_name = 'assignments/curator-assignment-delete.html'
    success_message = "Assignment successfully deleted!"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AssignmentDeleteView, self).delete(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data,
                                           suc_message="Assignment {0} successfully deleted".format(self.object.title))


class AssignmentListView(ListView):
    template_name = 'assignments/assignment-list.html'
    model = Assignment
    context_object_name = 'assignments'


class AssignmentDetailView(DetailView):
    template_name = 'assignments/assignment-form.html'
    model = Assignment
    context_object_name = 'assignment'

    # def get(self, request, *args, **kwargs):
    #     context = super(AssignmentDetailView, self).get(request)
    #     assignment_slug = self.kwargs['slug']
    #     user = self.request.user
    #
    #     try:
    #         assignment = Assignment.objects.get(slug=assignment_slug)
    #         stream = assignment.stream
    #     except Assignment.DoesNotExist:
    #         messages.add_message(self.request, messages.WARNING, "Assignment " + assignment_slug + " does not exist")
    #         raise Http404("Assignment does not exist")
    #
    #     if user not in stream.users.all() or user.is_staff:
    #         messages.add_message(self.request, messages.WARNING, 'This assignment is not available for you')
    #         raise Http404("This assignment is not available for you")
    #
    #     try:
    #         assignment_session = AssignmentSession.objects.get(user=user, assignment=assignment)
    #
    #     except AssignmentSession.DoesNotExist:
    #         if assignment.available_from > timezone.now():
    #             messages.add_message(self.request, messages.WARNING, 'This assignment is not available yet')
    #             raise Http404('This assignment is not available yet')
    #             # return redirect('process:index')
    #             # return HttpResponseRedirect(reverse('process:assignment_list'))
    #
    #         assignment_session = AssignmentSession.objects.create_session(user, assignment)
    #         assignment_session_question = AssignmentSessionQuestions.objects.create_session_question(assignment_session, assignment)
    #     print('qqq', assignment_session, assignment_session_question)
    #     question_index = assignment_session.current_index
    #     question_count = assignment_session.questions_amount
    #     assignment_end = assignment.available_from + datetime.timedelta(minutes=assignment.available_for_x_minutes)
    #
    #     if question_index >= question_count:
    #         # assignment_session.current_index = question_count
    #         # assignment_session.save()
    #         messages.add_message(self.request, messages.INFO, 'This assignment you already finished!')
    #
    #         raise Http404('This assignment you already finished!')
    #         # return redirect('process:index')
    #         # return HttpResponseRedirect(reverse('process:assignment_list'))
    #
    #     return context

    def get_context_data(self, **kwargs):
        context = super(AssignmentDetailView, self).get_context_data(**kwargs)
        assignment_slug = self.kwargs['slug']
        user = self.request.user

        try:
            assignment = Assignment.objects.get(slug=assignment_slug)
            stream = assignment.stream
        except Assignment.DoesNotExist:
            messages.add_message(self.request, messages.WARNING, "Assignment " + assignment_slug + " does not exist")
            raise Http404("Assignment does not exist")

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

        assignment = Assignment.objects.get(slug=assignment_slug)
        assignment_session = get_object_or_404(AssignmentSession, user=self.request.user, assignment=assignment)

        question_index = assignment_session.current_index
        question_count = assignment_session.questions_amount
        assignment_end = assignment_session.started_at + datetime.timedelta(minutes=assignment.available_for_x_minutes)
        session_end = assignment_session.started_at + datetime.timedelta(minutes=assignment.available_for_x_minutes)

        if question_index >= question_count or timezone.now() > assignment_end or timezone.now() > assignment_end:
            assignment_session.current_index = question_count
            assignment_session.save()
            messages.add_message(self.request, messages.INFO, 'This assignment you already finished!')

            raise Http404('This assignment you already finished!')
            # return redirect('process:index')
            # return HttpResponseRedirect(reverse('process:assignment_list'))

        # question_id = int(assignment_session.questions_amount.split(",")[question_index])
        question_list = AssignmentSessionQuestions.objects.filter(session=assignment_session)
        question_id_list = [q_id.id for q_id in question_list]
        print('question_id_list', question_id_list)
        question = AssignmentSessionQuestions.objects.get(id=question_id_list[question_index])
        # q = question.question
        context['started_at'] = assignment_session.started_at
        context['assignment_end'] = assignment_end
        context['question'] = question
        context['question_description'] = question.description

        context['progress'] = ProgressBar(question_index, question_count)
        context['form'] = AssignmentFormViewForm(self.request.GET or None)

        # if TopicList.is_differential_equation_with(question.topic.function_code):
        #     context['latex_question'] = latex(question.question[0])
        # elif TopicList.is_addition(question.topic.function_code):
        #     context['latex_question'] = latex(question.question)
        # elif TopicList.is_multiplication(question.topic.function_code):
        #     context['latex_question'] = latex(question.question)
        # elif TopicList.is_subtraction(question.topic.function_code):
        #     context['latex_question'] = latex(question.question)
        # elif TopicList.is_division(question.topic.function_code):
        #     context['latex_question'] = latex(question.question)
        # elif TopicList.is_differential_equation(question.topic.function_code):
        #     context['latex_question'] = latex(question.question)
        # else:
        #     context['latex_question'] = latex(eval(question.question))
        context['latex_question'] = convert_to_latex(question.topic.function_code, question.question)
        return context

    def form_invalid(self):
        return redirect(reverse('index'))


class AssignmentFormView(FormView):
    template_name = 'assignments/assignment-form.html'
    model = Assignment
    form_class = AssignmentFormViewForm
    context_object_name = 'assignment'

    def form_valid(self, form, **kwargs):
        context = super(AssignmentFormView, self).get_context_data(**kwargs)
        assignment_slug = self.kwargs['slug']
        print(assignment_slug)
        user = self.request.user
        try:
            assignment = get_object_or_404(Assignment, slug=assignment_slug)
        except Assignment.DoesNotExist:
            messages.add_message(self.request, messages.WARNING, "Assignment " + assignment_slug + " does not exist")
            raise Http404("Assignment " + assignment_slug + " does not exist")

        assignment_session = AssignmentSession.objects.get(assignment=assignment, user=user)
        question_index = assignment_session.current_index
        question_list = AssignmentSessionQuestions.objects.filter(session=assignment_session)
        question_id_list = [q_id.id for q_id in question_list]
        question_id = int(question_id_list[question_index])
        question = AssignmentSessionQuestions.objects.get(id=question_id)

        answer = form.cleaned_data['answer']
        question.user_answer = answer
        # questions_t_o_f() solve question and compare with user aswer and return True or False from givens
        question.is_correct = questions_t_o_f(question.topic.function_code, question.question, answer)
        # question_solver() solve question and return answers
        question.question_answer = question_solver(question.topic.function_code, question.question)
        question.finished_at = timezone.now()
        question.save()

        assignment_session.current_index += 1
        if question.is_correct is True:
            assignment_session.correct_answers += 1
        elif question.is_correct is False:
            assignment_session.incorrect_answers += 1
        else:
            raise Http404('Erorr please contact to developer!!!')
        assignment_session.save()

            # return redirect('/assignments/%s/' % assignment_slug)

        return redirect('/assignments/%s/' % assignment_slug)

    def get_success_url(self, **kwargs):
        return reverse_lazy('process:assignment_seshion_final', kwargs={'slug': self.kwargs['slug']})


class AssignmentSessionFinalView(DetailView):
    template_name = 'assignments/assignment-final.html'
    model = AssignmentSession
    context_object_name = 'result'


class AssignmentResultsListView(ListView):
    template_name = 'assignments/user-assignment-results-list.html'
    model = Assignment
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super(AssignmentResultsListView, self).get_context_data(**kwargs)
        user_assignments = AssignmentSession.objects.filter(user=self.request.user)
        context['user_assignments'] = user_assignments
        return context


class AssignmentResultDetailView(DetailView):
    template_name = 'assignments/user-assignment-result-detail.html'
    model = Assignment
    context_object_name = 'result'

    def get_context_data(self, **kwargs):
        context = super(AssignmentResultDetailView, self).get_context_data(**kwargs)
        messages.add_message(self.request, messages.INFO, 'This assignment you already finished!')
        session = get_object_or_404(AssignmentSession, user=self.request.user, assignment=kwargs['object'])
        # session = AssignmentSession.objects.filter(assignment=kwargs['object'])
        questions = AssignmentSessionQuestions.objects.filter(session=session)
        for question in questions:
            if question.user_answer is None or question.question_answer is None:
                question.question_answer = question_solver(question.topic.function_code, question.question)
                question.is_correct = False
                question.save()
        context['session'] = session.updated
        context['questions'] = questions
        return context


class CuratorAssignmentList(ListView):
    template_name = 'assignments/curator-assingment-list.html'
    model = Assignment
    context_object_name = 'supper_assignments'

    # def get_context_data(self, **kwargs):
    #     context = super(CuratorAssignmentList, self).get_context_data(**kwargs)
    #     context['supper_assignments'] = Assignment.objects.all()
    #     return context


class CuratorAssignmentSessionList(DetailView):
    template_name = 'assignments/curator-assingment-user-list.html'
    model = Assignment
    context_object_name = 'supper_assignments_session'

    def get_context_data(self, **kwargs):
        context = super(CuratorAssignmentSessionList, self).get_context_data(**kwargs)
        assignment_session_list = AssignmentSession.objects.filter(assignment=kwargs['object'])
        context['assignment_session_list'] = assignment_session_list
        return context


class CuratorAssignmentUserSessionResult(TemplateView):
    template_name = 'assignments/curator-assignment-user-detail.html'
    # model = AssignmentSessionQuestions
    # context_object_name = 'supper_sesion_result'

    def get_context_data(self, **kwargs):
        user = self.kwargs['pk']
        context = super(CuratorAssignmentUserSessionResult, self).get_context_data(**kwargs)
        assignment = get_object_or_404(Assignment, slug=self.kwargs['slug'])
        session = get_object_or_404(AssignmentSession, user=user, assignment=assignment)
        questions = AssignmentSessionQuestions.objects.filter(session=session)
        context['s_user'] = get_object_or_404(User, id=user)
        context['questions'] = questions
        context['result'] = session
        return context
