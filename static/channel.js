document.addEventListener('DOMContentLoaded', () => {

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, configure button(s)
  socket.on('connect', () => {

    // Signal server a user is connected
    socket.emit('joined');

    document.querySelector('#leave_channel').addEventListener('click', () => {
      socket.emit('left');
      window.location.replace('/');

      // Forget current channel when clicking 'Leave channel' button
      localStorage.removeItem('current_channel')
    });

    document.querySelector('#channels').addEventListener('click', () => {
      socket.emit('left');

      // Forget current channel when clicking 'Channels' button on the nav bar
      localStorage.removeItem('current_channel')

    });

    document.querySelector('#logout').addEventListener('click', () => {
      localStorage.removeItem('current_channel')
    });


    document.querySelector('#new_message').addEventListener("keydown", event =>{
      if (event.key == 'Enter') {
        document.querySelector('#send_button').click();
      }
      document.querySelector('#new_message').focus();
    });

    //document.querySelector('#logout').addEventListener('click', () => {
    //  localStorage.removeItem('current_channel')
    //});

    // send_button should emit a "submit message" event
    document.querySelector('#send_button').onclick = () => {
      const new_message = document.querySelector('#new_message').value;
      socket.emit('submit message', {'new_message': new_message.trim()});
      document.querySelector('#new_message').value = '';
    };

    // scrolling down
    var textarea = document.querySelector('#chat_area')
    textarea.scrollTop = textarea.scrollHeight;
  });

  // When a new message is announced, add to the textarea
  socket.on('announced message', data => {
    var textarea = document.querySelector('#chat_area');
    var new_message = data.new_message;
    textarea.value += new_message;
    textarea.scrollTop = textarea.scrollHeight;

  });

  //Announce a new user joined the channel, leave a notification in the chat_area
  socket.on('status_update', data => {
    let row =`${data.message}`
    document.querySelector('#chat_area').value += row + '\n';

    // scrolling down
    var textarea = document.querySelector('#chat_area')
    textarea.scrollTop = textarea.scrollHeight;

    // Save current channel on localStorage
    localStorage.setItem('current_channel', data.channel)
  })

});
