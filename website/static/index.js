async function deleteNote(noteId) {
  await fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    // window.location.href = "/";
    removeFadeOut(document.getElementById('row' + noteId), 500)
  })
}

// upadate DUEL

async function updateDuel(looopindex) {
  inputs = document.getElementById('checked[' + looopindex + ']')
  player = document.getElementById('player[' + looopindex + ']')
  duel = document.getElementById('duel[' + looopindex + ']')
  await fetch('/update-duel', {
    method: 'POST',
    body: JSON.stringify({
      duelCheck: inputs.checked + ',' + duel.value + ',' + player.value,
    }),
  }).then((_res) => {
    div1 = document.getElementById('confirmed[' + looopindex + ']')
    if (
      document.getElementById('checked[' + looopindex + ']').checked == true
    ) {
      div1.innerHTML = ''
    } else {
      var div1 = document.getElementById('confirmed[' + looopindex + ']')
      div1.innerHTML = '<h4>confirm</h4>'
    }

    inputs = null
    player = null
    duel = null

    // window.location.href = "/";
    //removeFadeOut(document.getElementById("row" + noteId), 500);
  })
}


async function viewGroup(group) {
  // var location_href = document.getElementById('view_group_'+group+'')
  // location_href.innerHTML =
  //   '<i class="fa fa-circle-o-notch fa-spin" style="margin-left:15px;padding:9px;"></i>'

  await fetch('/login', {
    method: 'POST',
    // body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    setTimeout(function(){
      // location_href.innerHTML = 'Free Demo'
      window.location.href = "/season/1/group/"+group+"";
    },500)
  })
}



async function locationHref(url) {
  var location_href = document.getElementById('location_href_'+url+'')
  var user = document.getElementById('user')
  // alert(user.value);
  location_href.innerHTML =
  '<i class="fa fa-circle-o-notch fa-spin" ></i>'
  
  await fetch('/login', {
    method: 'POST',
    // body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    setTimeout(function(){
      // location_href.innerHTML = 'Free Demo'
      // if(user){
        window.location.href = "/"+url+"";
        // location_href.innerHTML = '<i class="fa fa-circle-o-notch fa-spin" style="transition-duration: 3s;opacity:0;margin-left:15px;padding:9px;"></i>'
      // }else{
      //   window.location.href = "/"+url+"";
      //   location_href.innerHTML = '<i class="fa fa-circle-o-notch fa-spin" style="transition-duration: 3s;opacity:0;margin-left:15px;padding:9px;"></i>'
      // }
    },500)
  })
}

async function updateDuel2(looopindex) {
  const body = document.body
  var result = document.getElementById('user_duel_result[' + looopindex + ']')
  var player = document.getElementById('user_duel_id[' + looopindex + ']')
  var duel = document.getElementById('duel_id[' + looopindex + ']')
  if (looopindex == 1) {
    var result_oponent = document.getElementById('user_duel_result[2]')
    var player_oponent = document.getElementById('user_duel_id[2]')
    var duel_oponent = document.getElementById('duel_id[2]')
  } else {
    var result_oponent = document.getElementById('user_duel_result[1]')
    var player_oponent = document.getElementById('user_duel_id[1]')
    var duel_oponent = document.getElementById('duel_id[1]')
  }
  // alert(result.value)

  var spin = document.getElementById('updateDuelButton[' + looopindex + ']')

  if (
    result.value >= 0 &&
    result.value <= 6 &&
    (result.value != result_oponent.value || result.value == 0)
  ) {
    spin.innerHTML =
      '<i class="fa fa-circle-o-notch fa-spin" style="margin-left:15px;"></i>'
    time = 500
  } else {
    spin.innerHTML = 'OUT OF RANGE'
    setInterval(function () {
      spin.innerHTML = 'SUBMIT'
    }, 2600)
    return false
  }

  if (
    result_oponent.value >= 0 &&
    result_oponent.value <= 6 &&
    (result.value != result_oponent.value || result.value == 0)
  ) {
    spin.innerHTML =
      '<i class="fa fa-circle-o-notch fa-spin" style="margin-left:15px;"></i>'
    var time = 500
  } else {
    spin.innerHTML = 'OUT OF RANGE'
    setInterval(function () {
      spin.innerHTML = 'SUBMIT'
    }, 2600)
    return false
  }

  // alert(result_oponent.value)
  // alert(player_oponent.value)
  // alert(duel_oponent.value)

  // spin = document.getElementById('spin-result-update[' + looopindex + ']')

  await fetch('/update-duel2', {
    method: 'POST',
    body: JSON.stringify({
      duelResult:
        result.value +
        ',' +
        duel.value +
        ',' +
        player.value +
        ',' +
        result_oponent.value +
        ',' +
        duel_oponent.value +
        ',' +
        player_oponent.value,
    }),
  }).then((_res) => {
    player_name_result = document.getElementById(
      'player-name-result[' + looopindex + ']',
    )

    ele = document.getElementById('user_duel_result[' + looopindex + ']')
    ele.style.visibility = ele.style.visibility == 'visible' ? '' : 'hidden'

    setInterval(function () {
      ele.style.visibility = ele.style.visibility == 'hidden' ? '' : 'visible'
    }, 200)

    setInterval(function () {
      spin.innerHTML = 'SUBMIT'
    }, 500)

    // alert(duelCheck)
    // window.location.href = "/";
    //removeFadeOut(document.getElementById("row" + noteId), 500);
  })
}
// var checkedValue = document.querySelector('.messageCheckbox:checked').value;

// #### chooseGroup

async function chooseGroup(looopindex) {
  var grno = document.getElementById('grno[' + looopindex + ']')
  var grname = document.getElementById('grname[' + looopindex + ']')
  var seasons = document.getElementById('seasons[' + looopindex + ']')

  await fetch('/season/' + seasons.value + '/group/' + grno.value + '', {
    method: 'POST',
    body: JSON.stringify({
      groupList: grno.value + ',' + grname.value + ',' + seasons.value,
    }),
  }).then((_res) => {
    console.log(_res)
    // $("#duels-list").load('/season/'+seasons.value+'/group/'+groupId+'');
    // window.location.href = "/";
    // removeFadeOut(document.getElementById('row' + duelId), 500)
  })
}

async function deleteDuel(duelId) {
  await fetch('/delete-duel', {
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

document.getElementsByClassName('resultscore').onclick = function () {
  this.select()
}

function GoBackWithRefresh(event) {
  if ('referrer' in document) {
    window.location = document.referrer
    /* OR */
    //location.replace(document.referrer);
  } else {
    window.history.back()
  }
}

//CAROUSEL
// const myCarouselElement = document.querySelector('#carouselExampleControls')
// const carousel = new bootstrap.Carousel(myCarouselElement, {
//   interval: 2000,
//   wrap: false
// })
