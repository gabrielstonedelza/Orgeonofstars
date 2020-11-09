// document.querySelector("#connect").addEventListener('click',()=>{
//     start_conference()
// })

// var peers_lists = []

// function start_conference(){
//     navigator.mediaDevices.getUserMedia({
//         video: true,
//         audio: true
//       }).then(gotMedia).catch(() => {})

//       function gotMedia (stream) {
//         // var peer1 = new SimplePeer({ initiator: true, stream: stream })
//         // var peer2 = new SimplePeer()

//         // for (const ele of peers_lists){
//         //     ele = new SimplePeer()
//         // }

//         // peer1.on('signal', data => {
//         //   peer2.signal(data)
//         // })

//         // peer2.on('signal', data => {
//         //   peer1.signal(data)
//         //   peers_lists.push(JSON.stringify(data))
//         // })

//           // got remote video stream, now let's show it in a video tag
//           var video = document.querySelector('video')

//           if ('srcObject' in video) {
//             video.srcObject = stream
//           } else {
//             video.src = window.URL.createObjectURL(stream) // for older browsers
//           }

//           video.play()
//       }
// }

// document.querySelector("#connect").addEventListener("click", () => {
//   navigator.getUserMedia({ audio: true, video: true }, gotStream, onfail);
// });

// function gotStream(stream) {
//   console.log("The connection is set");
//   window.AudioContext = window.AudioContext || window.webkitAudioContext;
//   var audioContext = new AudioContext();
//   // Create an AudioNode from the stream
//   var mediaStreamSource = audioContext.createMediaStreamSource(stream);
//   // Connect it to destination to hear yourself
//   // or any other node for processing!
//   mediaStreamSource.connect(audioContext.destination);
//   var video = document.querySelector("video");
//   var videoTracks = stream.getVideoTracks();
 
//   window.stream = stream; // make variable available to browser console
//   video.srcObject = stream;
// }
// function onfail(error) {
//   console.log(
//     "permission not granted or system don't have mediadevices." + error.name
//   );
// }
