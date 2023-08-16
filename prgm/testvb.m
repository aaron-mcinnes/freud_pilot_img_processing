recorder = actxserver('VisionRecorder2.EEGRecorder');
recorder.RecordingFile = 'C:\path\to\file.eeg';
recorder.StartRecording();

recorder.StopRecording();