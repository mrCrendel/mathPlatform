function getIsUserEnrolledUrl(streamCode) {
  return `/subject/stream/${streamCode}/is-enrolled`;
}

function getEnrollUserUrl() {
  return `/subject/stream/enroll_user/`;
}

function loadStreamDetailsPage() {

}

function isUserEnrolled(data = {}) {
  var userId = null;
  var streamCode = null;
  if (data.hasOwnProperty('userId')) {
    userId = data['userId'];
  }
  if (data.hasOwnProperty('streamCode')) {
    streamCode = data['streamCode'];
  }
  if (isEmptyVar(streamCode)) {
    streamCode = getPrimaryCode();
  }
  if (isEmptyVar(streamCode)) {
    return responseError({
      errorMessage: "No stream code is provided"
    });
  }
  var result = postAjax(getIsUserEnrolledUrl(streamCode));
  return result;
}

function displayEnrollAccess(isEnrolled) {
  if (isEnrolled) {
    $('#enrolled-section').removeAttr('hidden');
  }
  if (!isEnrolled) {
    $('#not-enrolled-section').removeAttr('hidden');
  }
}

function enrollRequest(data) {
  if (data == null) {
    return {
      'errorMessage': 'Invalid data'
    }
  }
  if (!data.hasOwnProperty('streamCode')) {
    data['streamCode'] = getPrimaryCode();
  }
  return postAjax(getEnrollUserUrl(), data);
}

function enrollUser(enrollKey, userId = 0) {
  var data = {
    userId: userId,
    enrollKey: enrollKey,
    enrollOperation: true
  };
  return enrollRequest(data);
}

function unEnrollUser(userId = 0) {
  var data = {
    userId: userId,
    enrollOperation: false
  };
  return enrollRequest(data);
}

function getAssignments(data = {}) {
  if (!data.hasOwnProperty('userId')) {
    data['userId'] = 0;
  }
  var response = postAjax(`/subject/assignments/`, data);
  return response['assignments'];
}

function getExams(data = {}) {
  if (!data.hasOwnProperty('userId')) {
    data['userId'] = 0;
  }
  data['isExam'] = true;
  var response = postAjax(`/subject/assignments/`, data);
  return response['assignments'];
}

function getStreamAssignmentsDetails(streamCode, userId = 0) {
  if (isEmptyVar(streamCode)) {
    streamCode = getPrimaryCode();
  }
  var data = {
    userId: userId,
    streamCode: streamCode
  };
  var assignment = getAssignments(data);
  return assignment;
}

function getStreamExamDetails(streamCode, userId = 0) {
  if (isEmptyVar(streamCode)) {
    streamCode = getPrimaryCode();
  }
  var data = {
    userId: userId,
    streamCode: streamCode
  };
  var exam = getExams(data);
  return exam;
}

function dislpayStreamAssignmentDetails(ass, isExam = false) {
  if (null == ass) {
    ass = getStreamAssignmentsDetails();
  }
  if (null == ass) {
    return;
  }
  var out = '';
  ass.forEach((ass) => {
    out += `<ul class="assignment-list">`;
    out += `<li class="font-weight-bold">${ass.assignmentName}: ${ass.solvedCount}/${ass.examplesCount}</li>`;
    if (!ass.hasOwnProperty("assignments") || ass.assignments == null) {
      return;
    }
    ass.assignments.forEach(it => {
      var assignmentDone = getAssignmentDoneById(ass.assignmentsDone, it.assignmentTopicId);
      out += `<a href="/subject/show-assignment/${it.assignmentTopicId}"><li id="${it.id}">${it.topicCode}: `;
      if (assignmentDone == null) {
        out += `(0/${it.exampleAmount}) `;
      } else if (assignmentDone != null) {
        if (assignmentDone.isDone || assignmentDone.exampleAmount >= it.exampleAmount) {
          out += `(${it.exampleAmount}/${it.exampleAmount})`;
          out += ` [OK]`;
        } else {
          out += `(${assignmentDone.exampleAmount}/${it.exampleAmount})`;
        }
      }

      out += `</li></a>`
    });
    out += `</ul>`

  });
  if (!isExam) {
    $("#assignments").html($("#assignments").html() + out);
    $("#assignments-title").removeAttr("hidden");
  } else {
    $("#exams").html($("#exams").html() + out);
    $("#exams-title").removeAttr("hidden");
  }
}

function getAssignmentDoneById(list, topicId) {{
  if (list == null || list.length == 0) {
    return null;
  }
  for (var obj of list) {
    if (obj.assignmentTopicId === topicId)
      return obj;
    }
  }
  return null;
}

function getAssignmentDetails(streamId) {
  if (isNaN(streamId)) {
    streamId = getPrimaryCode();
  }
  var result = ajaxGet(`/subject/get-assignment-details/${streamId}`);
  return result;
}

// /subject/show-assignment/{assignmentTopicId}/ => show assignment  page
// /subject/get-assignment/{assignmentTopicId}/