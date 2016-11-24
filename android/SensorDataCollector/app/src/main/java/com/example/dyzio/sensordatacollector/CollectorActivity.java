package com.example.dyzio.sensordatacollector;

import android.Manifest;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Build;
import android.os.Environment;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.IOException;
import java.io.FileWriter;


public class CollectorActivity extends AppCompatActivity implements SensorEventListener {
    private static final int REQUEST_WRITE_EXTERNAL_STORAGE = 112;
    private static String LOG_TAG = "SensorDataCollectorLog";
    private static String DIR_NAME = "SensorDataCollector";
    private static int SAMPLING_RATE = 20000;        // time for sample in us
    private static int TIMESTAMP_DIVIDER = 1000000;  // convert timestamp from ns to ms
    private static String STANDBY_MESSAGE = "Choose your mean of transport to start collecting data.";
    private static String COLLECTING_DATA_MESSAGE = "Collecting data... To stop click on selected mean of transport.";

    private File accelerometerFile = null;
    private File gyroscopeFile = null;
    private boolean isExternalStorageWritable = Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState());
    private SensorManager sensorManager;
    private Sensor accelerometer = null;
    private Sensor gyroscope = null;
    private boolean collectingData = false;
    private long firstTimestamp = 0;
    private String meanOfTransport = "";

    private TextView message;
    private Button bus;
    private Button car;
    private Button train;
    private Button tram;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_collector);

        message = (TextView) findViewById(R.id.textViewMessage);
        bus = (Button) findViewById(R.id.buttonCollectBus);
        car = (Button) findViewById(R.id.buttonCollectCar);
        train = (Button) findViewById(R.id.buttonCollectTrain);
        tram = (Button) findViewById(R.id.buttonCollectTram);

        message.setText(STANDBY_MESSAGE);

        if (Build.VERSION.SDK_INT >= 23) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, REQUEST_WRITE_EXTERNAL_STORAGE);
        }

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        if (accelerometer != null) {
            sensorManager.registerListener(this, accelerometer, SAMPLING_RATE);
        } else {
            Log.d(LOG_TAG, "There is no accelerometer.");
        }

        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        if (gyroscope != null) {
            sensorManager.registerListener(this, gyroscope, SAMPLING_RATE);
        } else {
            Log.d(LOG_TAG, "There is no gyroscope.");
        }

        if (isExternalStorageWritable) {
            File dir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS), DIR_NAME);
            if (!dir.exists()) {
                dir.mkdirs();
                Log.d(LOG_TAG, "Directory created.");
            } else {
                Log.d(LOG_TAG, "Directory already exists.");
            }
            if (accelerometer != null) {
                accelerometerFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS) + "/" + DIR_NAME, "accelerometer.csv");
                if (!accelerometerFile.exists()) {
                    try {
                        accelerometerFile.createNewFile();
                        Log.d(LOG_TAG, "Accelerometer data file created.");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } else {
                    Log.d(LOG_TAG, "Accelerometer data file already exists.");
                }
            }
            if (gyroscope != null) {
                gyroscopeFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS) + "/" + DIR_NAME, "gyroscope.csv");
                if (!gyroscopeFile.exists()) {
                    try {
                        gyroscopeFile.createNewFile();
                        Log.d(LOG_TAG, "Gyroscope data file created.");
                    } catch (IOException e) {
                        Log.e(LOG_TAG, "File creating failed: " + e.toString());
                    }
                } else {
                    Log.d(LOG_TAG, "Gyroscope data file already exists.");
                }
            }
        }
    }

    private void toggleCollectingData() {
        collectingData = !collectingData;

        if (collectingData) {
            Log.d(LOG_TAG, "Starting collecting data.");
            message.setText(COLLECTING_DATA_MESSAGE);
        } else {
            Log.d(LOG_TAG, "Stopping collecting data.");
            message.setText(STANDBY_MESSAGE);
            firstTimestamp = 0;
        }
    }

    public void onButtonCollectBusClick(View v) {
        toggleCollectingData();

        int visibility = collectingData ? Button.INVISIBLE : Button.VISIBLE;
        car.setVisibility(visibility);
        train.setVisibility(visibility);
        tram.setVisibility(visibility);

        meanOfTransport = "BUS";
    }

    public void onButtonCollectCarClick(View v) {
        toggleCollectingData();

        int visibility = collectingData ? Button.INVISIBLE : Button.VISIBLE;
        bus.setVisibility(visibility);
        train.setVisibility(visibility);
        tram.setVisibility(visibility);

        meanOfTransport = "CAR";
    }

    public void onButtonCollectTrainClick(View v) {
        toggleCollectingData();

        int visibility = collectingData ? Button.INVISIBLE : Button.VISIBLE;
        bus.setVisibility(visibility);
        car.setVisibility(visibility);
        tram.setVisibility(visibility);

        meanOfTransport = "TRAIN";
    }

    public void onButtonCollectTramClick(View v) {
        toggleCollectingData();

        int visibility = collectingData ? Button.INVISIBLE : Button.VISIBLE;
        bus.setVisibility(visibility);
        car.setVisibility(visibility);
        train.setVisibility(visibility);

        meanOfTransport = "TRAM";
    }

    public void onButtonClearDataClick(View v) {
        if (accelerometerFile != null && accelerometerFile.exists()) {
            accelerometerFile.delete();
            Log.d(LOG_TAG, "Accelerometer data file deleted.");
        }
        if (gyroscopeFile != null && gyroscopeFile.exists()) {
            gyroscopeFile.delete();
            Log.d(LOG_TAG, "Gyroscope data file deleted.");
        }

        Toast.makeText(this, "Data deleted.", Toast.LENGTH_SHORT).show();
    }

    public void onButtonSendDataClick(View v) {

    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (collectingData) {
            if (firstTimestamp == 0) {
                firstTimestamp = Math.round((double)event.timestamp/TIMESTAMP_DIVIDER);
            }
            if (event.sensor.equals(accelerometer)) {
                try {
                    FileWriter fileWriter = new FileWriter(accelerometerFile, true);
                    fileWriter.append(meanOfTransport + "," + (Math.round((double)event.timestamp/TIMESTAMP_DIVIDER) - firstTimestamp) + "," + event.values[0] + "," + event.values[1] + "," + event.values[2] + System.getProperty("line.separator"));
                    fileWriter.flush();
                    fileWriter.close();
                } catch (IOException e) {
                    Log.e(LOG_TAG, "Write to file failed: " + e.toString());
                }
            } else if (event.sensor.equals(gyroscope)) {
                try {
                    FileWriter fileWriter = new FileWriter(gyroscopeFile, true);
                    fileWriter.append(meanOfTransport + "," + (Math.round((double)event.timestamp/TIMESTAMP_DIVIDER) - firstTimestamp) + "," + event.values[0] + "," + event.values[1] + "," + event.values[2] + System.getProperty("line.separator"));
                    fileWriter.flush();
                    fileWriter.close();
                } catch (IOException e) {
                    Log.e(LOG_TAG, "Write to file failed: " + e.toString());
                }
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        if (collectingData) {
            Log.d(LOG_TAG, sensor.getName() + " changed accuracy to " + accuracy + ".");
        }
    }
}
