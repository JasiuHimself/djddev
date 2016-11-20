package com.example.dyzio.sensordatacollector;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import java.io.File;
import java.io.IOException;
import java.io.FileWriter;


public class CollectorActivity extends AppCompatActivity implements SensorEventListener {
    private String LOG_TAG = "SensorDataCollectorLog";
    private String DIR_NAME = "SensorDataCollector";
    public int SAMPLING_RATE = 20000;
    private File accelerometerFile = null;
    private File gyroscopeFile = null;
    private boolean isExternalStorageWriteable = Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState());
    private SensorManager sensorManager;
    private Sensor accelerometer = null;
    private Sensor gyroscope = null;
    private boolean collectingData = false;
    private long firstTimestamp = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_collector);

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

        if (isExternalStorageWriteable) {
            File dir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS), DIR_NAME);
            if (!dir.exists()) {
                dir.mkdirs();
                Log.d(LOG_TAG, "Directory created.");
            } else {
                Log.d(LOG_TAG, "Directory already exists.");
            }
            if (accelerometer != null) {
                accelerometerFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS) + "/" + DIR_NAME, "accelerometer.txt");
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
                gyroscopeFile = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS) + "/" + DIR_NAME, "gyroscope.txt");
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

    public void onButtonCollectDataClick(View v) {
        collectingData = !collectingData;

        if (collectingData) {
            Log.d(LOG_TAG, "Starting collecting data.");
        } else {
            Log.d(LOG_TAG, "Stopping collecting data.");
            firstTimestamp = 0;
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (collectingData) {
            if (firstTimestamp == 0) {
                firstTimestamp = Math.round((double)event.timestamp/1000000);   // convert timestamp to milliseconds
            }
            if (event.sensor.equals(accelerometer)) {
                try {
                    FileWriter fileWriter = new FileWriter(accelerometerFile, true);
                    fileWriter.append(event.values[0] + " " + event.values[1] + " " + event.values[2] + " " + (Math.round((double)event.timestamp/1000000) - firstTimestamp) + System.getProperty("line.separator"));
                    fileWriter.flush();
                    fileWriter.close();
                } catch (IOException e) {
                    Log.e(LOG_TAG, "File write failed: " + e.toString());
                }
            } else if (event.sensor.equals(gyroscope)) {
                try {
                    FileWriter fileWriter = new FileWriter(accelerometerFile, true);
                    fileWriter.append(event.values[0] + " " + event.values[1] + " " + event.values[2] + " " + (Math.round((double)event.timestamp/1000) - firstTimestamp) + System.getProperty("line.separator"));
                    fileWriter.flush();
                    fileWriter.close();
                } catch (IOException e) {
                    Log.e(LOG_TAG, "File write failed: " + e.toString());
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
