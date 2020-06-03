if (localStorage.getItem('current_channel')) {
  if ('undefined' != localStorage.getItem('current_channel')) {
    var channel = localStorage.getItem('current_channel');
    window.location.replace('/channel/' + channel);
  }
}
