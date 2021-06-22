function getTimeRemaining(endtime) {
  const total = Date.parse(endtime) - Date.parse(new Date());
  const seconds = Math.floor((total / 1000) % 60);
  const minutes = Math.floor((total / 1000 / 60) % 60);
  const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
  const days = Math.floor(total / (1000 * 60 * 60 * 24));

  return {
    total,
    days,
    hours,
    minutes,
    seconds
  };
}

function initializeClock(id, endtime) {
  const clock = document.getElementById(id);
  const daysSpan = clock.querySelector('.days');
  const hoursSpan = clock.querySelector('.hours');
  const minutesSpan = clock.querySelector('.minutes');
  const secondsSpan = clock.querySelector('.seconds');

  function updateClock() {
    const t = getTimeRemaining(endtime);

//    daysSpan.innerHTML = t.days;
    hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
    minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
    secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

    if (t.total <= 0) {
      clearInterval(timeinterval);
    }
  }

  updateClock();
  const timeinterval = setInterval(updateClock, 1000);
}

const timelimit = document.getElementById('time-limit-in-minutes')

if (timelimit) {
    const deadline = new Date(Date.parse(new Date()) + JSON.parse(timelimit.textContent) * 60 * 1000);
    initializeClock('clockdiv', deadline);
}

$('#challengeForm').submit(function(e){
//  handle incorrect answers do not rerender the form
    let form = this;
    e.preventDefault();
    $.ajax({
        type: form.method,
        url: form.action,
        data: $('#challengeForm').serialize(),
        success: function(data){
            location.href = '/'
        },
        error: function () {
            // Fail message
            $("#success").html("<div class='alert alert-danger'>");
            $("#success > .alert-danger")
                .html(
                    "<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;"
                )
                .append("</button>");
            $("#success > .alert-danger").append(
                $("<strong>").text(
                    "Ooops, that's not correct or time is up. Please try again!"
                )
            );
            $("#success > .alert-danger").append("</div>");
        },
    });
});