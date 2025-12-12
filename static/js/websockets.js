var is_chairperson = ($('input[name="chairperson_check"]').val().toLowerCase() === 'true');
var is_board_member = ($('input[name="member_check"]').val().toLowerCase() === 'true');
var is_secretary = ($('input[name="secretary_check"]').val().toLowerCase() === 'true');

var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

const stagingSocket = new WebSocket(
  ws_scheme + '://'
  + window.location.host
  + '/ws/recruitment/staging/'
);

const assentingSocket = new WebSocket(
  ws_scheme + '://'
  + window.location.host
  + '/ws/recruitment/assenting/'
);

const approvalSocket = new WebSocket(
  ws_scheme + '://'
  + window.location.host
  + '/ws/recruitment/approval/'
);

stagingSocket.onmessage = function (e) {
  if (is_board_member) {
    $('#shortlisting-modal').modal('show');

    const data = JSON.parse(e.data);

    var candidates_data = data['candidates']
    var list = [];

    for (var i = 0; i < candidates_data.length; i++) {
      list.push(candidates_data[i].fields)
    }

    var vacancy = data['vacancy'].fields.name;
    var vacancy_id = data['vacancy'].pk;
    var vacancy_next_action = data['vacancy'].next_action

    $('span#vacancy_name').each(function () { $(this).text(vacancy); });

    $(function () {
      $('#shortlisting-table tbody').html("");
      $.each(list, function (i, item) {
        var $tr = $('<tr>').append(
          $('<td>').text(item.first_name + " " + item.other_names + " " + item.last_name),
          $('<td>').text(item.id_number),
          $('<td>').text(item.gender),
          $('<td>').text(item.phone),
        );

        $('#shortlisting-table tbody').append($tr);
      });

      $('#shortlisting-table').dataTable();
    });

    var review_exists = data['review_exists'];
    var candidates_id_array = [];
    var current_url = window.location.href + '/' + vacancy_next_action + '/';
    var redirect_url = current_url.replace("applicants", "awaiting_room");

    for (var i = 0; i < list.length; i++) {
      candidates_id_array.push(candidates_data[i].pk);
    }

    if (!review_exists) {
      $('#assent-btn').click(function () {
        assentingSocket.send(JSON.stringify({
          'action_type': vacancy_next_action,
          'vacancy': vacancy_id,
          'candidates': candidates_id_array,
          'consent': true,
        }));
        // $('#shortlisting-modal').modal('hide');
      });
      $('#dissent-btn').click(function () {
        assentingSocket.send(JSON.stringify({
          'action_type': vacancy_next_action,
          'vacancy': vacancy_id,
          'candidates': candidates_id_array,
          'consent': false,
        }));
        // $('#shortlisting-modal').modal('hide');
      });
    } else {
      $('#affirmatory-text').html(
        'You have already given your feedback regarding the staging of the following candidates.'
      );
      $('#call-to-action').html(
        '<div class="mr-auto">\
          <span class="font-weight-bold text-danger">You have already reviewed this vacancy</span>\
        </div>\
        <a href='+ redirect_url + ' class="btn btn-outline-primary">Go to awaiting room</a>'
      );
    }
  };
}

assentingSocket.onmessage = function (e) {
  if (is_board_member) {
    const data = JSON.parse(e.data);
    switch (data.msg_type) {
      case 'notify_members':
        var location = window.location.href;
        var swal_func = function () {
          if (data.sender) {
            $('#shortlisting-modal').modal('hide');
            Swal.fire({
              type: 'success',
              title: data.message,
              position: 'bottom-start',
              toast: true,
              confirmButtonText: "&times;",
              timer: 2000,
              timerProgressBar: true,
            }).then((result) => {
              if (result.isConfirmed || result.dismiss === Swal.DismissReason.timer) {
                window.location = '/recruitment/vacancies/' + data.vacancy_id + '/awaiting_room/' + data.action_type + '/';
              }
            });
          } else {
            Swal.fire({
              type: 'success',
              title: data.message,
              position: 'bottom-start',
              toast: true,
              confirmButtonText: "&times;",
              timer: 2000,
              timerProgressBar: true,
            });
          }
        }

        swal_func();
        break;
      case 'approve_action':
        $('#approval-modal').modal('show');
        var approvers_data = JSON.parse(data['consentees']);
        var candidates_data = JSON.parse(data['candidates']);
        var vacancy = data['vacancy'].fields.name;
        var candidates_count = candidates_data.length;

        $('span#vacancy_name').each(function () { $(this).text(vacancy); });
        $('span#candidates_count').text(candidates_count)

        for (var i = 0; i < approvers_data.length; i++) {
          counter = i + 1;
          $("#approvers").append('<li class="list-group-item">' + counter + ". " + approvers_data[i].user__first_name + " " + approvers_data[i].user__last_name + '</li>');
        }

        $('#candidates-section').hide();
        $('#display-candidates').click(function () {
          $('#candidates-section').toggle('show');
        });

        $(function () {
          $('#candidates-table tbody').html("");

          var candidates_list = [];

          for (var i = 0; i < candidates_data.length; i++) {
            candidates_list.push(candidates_data[i].fields)
          }

          $.each(candidates_list, function (i, item) {
            var $tr = $('<tr>').append(
              $('<td>').text(item.first_name + " " + item.other_names + " " + item.last_name),
              $('<td>').text(item.id_number),
              $('<td>').text(item.gender),
              $('<td>').text(item.phone),
            );

            $('#candidates-table tbody').append($tr);
          });

          $('#candidates-table').dataTable();
        });

        if (is_chairperson) {
          var candidates_pks = []
          for (var i = 0; i < candidates_data.length; i++) {
            candidates_pks.push(candidates_data[i].pk)
          }

          $('#approve-btn').click(function () {
            approvalSocket.send(JSON.stringify({
              'vacancy_id': data['vacancy'].pk,
              'candidates_pks': candidates_pks,
              'action_type': data['vacancy'].next_action,
              'approval': true
            }));
          });
          $('#disapprove-btn').click(function () {
            // Dissaprove action
          });
        }
        break;
      default:
        console.log("No type specified")
    }
  }
}

approvalSocket.onmessage = function (e) {
  if (is_board_member) {
    $('#approval-modal').modal('hide');
    const data = JSON.parse(e.data);
    console.log(data.review_type);
    var swal_func = function () {
      Swal.fire({
        type: 'success',
        title: data.message,
        position: 'bottom-start',
        toast: true,
        confirmButtonText: "&times;",
        timer: 2000,
        timerProgressBar: true,
      }).then((result) => {
        if (result.isConfirmed || result.dismiss === Swal.DismissReason.timer) {
          if (data.review_type === 'shortlist') {
            window.location = '/recruitment/vacancies/' + data.vacancy_id + '/applicants/shortlisted-candidates/';
          }
          else if (data.review_type === 'appointment') {
            window.location = '/recruitment/vacancies/' + data.vacancy_id + '/applicants/appointed-candidates/';
          }
        }
      });
    }
    swal_func();
  }
}
