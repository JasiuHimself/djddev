package dawidperdek.djddev.smartbandapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    public void loginAttempt(View view) {
        String login = ((EditText)findViewById(R.id.editTextUserLogin)).getText().toString();
        String password = ((EditText)findViewById(R.id.editTextUserPassword)).getText().toString();
        if (checkCredentials(login, password)) {
            final Intent in = new Intent(this, UserMainActivity.class);
            startActivity(in);
        }
        else {
            Toast.makeText(this, "Wrong login or password.", Toast.LENGTH_SHORT).show();
        }
    }

    private boolean checkCredentials(String login, String password) {
        return login.equalsIgnoreCase(password);
    }
}
