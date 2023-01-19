function deleteNote(noteId) {
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    // window.location.href = "/";
    removeFadeOut(document.getElementById('row' + noteId), 500)
  })
}

// upadate DUEL

function updateDuel(looopindex) {
  inputs = document.getElementById('checked[' + looopindex + ']')
  player = document.getElementById('player[' + looopindex + ']')
  duel = document.getElementById('duel[' + looopindex + ']')
  fetch('/update-duel', {
    method: 'POST',
    body: JSON.stringify({
      duelCheck: inputs.checked + ',' + duel.value + ',' + player.value,
    }),
  }).then((_res) => {
    inputs = null
    player = null
    duel = null
    // alert(duelCheck)
    // window.location.href = "/";
    //removeFadeOut(document.getElementById("row" + noteId), 500);
  })
}

function updateDuel2(looopindex) {
  const body = document.body
  var result = document.getElementById('user_duel_result[' + looopindex + ']')
  var player = document.getElementById('user_duel_id[' + looopindex + ']')
  var duel = document.getElementById('duel_id[' + looopindex + ']')

  // alert(result.value)
  fetch('/update-duel2', {
    method: 'POST',
    body: JSON.stringify({
      duelResult: result.value + ',' + duel.value + ',' + player.value,
    }),
  }).then((_res) => {
    // body.append('<div class="alert success"></div>');

    ele = document.getElementById('user_duel_result[' + looopindex + ']')
    ele.style.visibility = ele.style.visibility == 'visible' ? '' : 'hidden'

    setInterval(function () {
      ele.style.visibility = ele.style.visibility == 'hidden' ? '' : 'visible'
    }, 200)
    // alert(duelCheck)
    // window.location.href = "/";
    //removeFadeOut(document.getElementById("row" + noteId), 500);

  })
}
// var checkedValue = document.querySelector('.messageCheckbox:checked').value;

function deleteDuel(duelId) {
  fetch('/delete-duel', {
    method: 'POST',
    body: JSON.stringify({ duelId: duelId }),
  }).then((_res) => {
    // window.location.href = "/";
    removeFadeOut(document.getElementById('row' + duelId), 500)
  })
}

function removeFadeOut(el, speed) {
  var seconds = speed / 1000
  el.style.transition = 'opacity ' + seconds + 's ease'

  el.style.opacity = 0
  setTimeout(function () {
    el.parentNode.removeChild(el)
  }, speed)
}

// var xhr = new XMLHttpRequest();
// xhr.open("GET", "pythoncode.py?text=" + text, true);
// xhr.responseType = "JSON";
// xhr.onload = function(e) {
//   var arrOfStrings = JSON.parse(xhr.response);
// }
// xhr.send();


document.getElementsByClassName("resultscore").onclick = function() {
    this.select();
};
