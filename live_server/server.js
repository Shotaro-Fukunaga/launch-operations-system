const http = require('http');
const socketIo = require('socket.io');
const { spawn } = require('child_process');

const server = http.createServer();
const io = socketIo(server, {
  cors: {
    origin: "*", // 必要に応じてCORSポリシーを設定
    methods: ["GET", "POST"]
  }
});

io.on('connection', (socket) => {
  console.log('New client connected');

  socket.on('start-stream', () => {
    // FFmpegプロセスを起動してRTMPストリームをWebRTCに変換する
    const ffmpeg = spawn('ffmpeg', [
      '-i', 'rtmp://localhost:1935/live', // RTMPストリームの入力URL
      '-c:v', 'libx264',
      '-preset', 'ultrafast',
      '-tune', 'zerolatency',
      '-c:a', 'aac',
      '-f', 'mpegts',
      '-',
    ]);

    ffmpeg.stdout.on('data', (data) => {
      socket.emit('video', data);
    });

    ffmpeg.stderr.on('data', (data) => {
      console.error(`FFmpeg error: ${data}`);
    });

    ffmpeg.on('close', (code) => {
      console.log(`FFmpeg process closed with code ${code}`);
    });

    socket.on('disconnect', () => {
      console.log('Client disconnected');
      ffmpeg.kill('SIGINT');
    });
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

server.listen(8010, () => {
  console.log('Listening on port 8010');
});
