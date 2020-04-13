package com.dsimutin.invapp;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class UserActivity extends AppCompatActivity {

    EditText task_text;
    EditText summary;
    Button b;

    String apiUrl = "";
    String apiToken = "";
    int computer_id, user_id;
    Intent intent;
    RequestQueue requestQueue;

    protected void postTask() {
        String url = apiUrl + "/tasks";
        JSONObject payload = new JSONObject();
        try {
            payload.put("body", task_text.getText());
            payload.put("summary", summary.getText());
            payload.put("linked_to", computer_id);
            payload.put("user_id", user_id);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        final VolleyResponseListener v_listener = new VolleyResponseListener() {
            @Override
            public void onError() {
                Log.e("LISTENER", "onError: FAILURE");
            }

            @Override
            public void onResponse() {
                Context context = getApplicationContext();
                CharSequence text = "SUCCESSFULLY SENT";
                int duration = Toast.LENGTH_SHORT;

                Toast toast = Toast.makeText(context, text, duration);
                toast.show();
            }
        };
        JsonRequest request = new JsonRequest
                (Request.Method.POST, url, v_listener, payload, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        JSONObject headers = new JSONObject();
                        try {
                            headers = response.getJSONObject("headers");

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        try {
                            String str = headers.getString("Set-Cookie");
                            apiToken = str.split(";")[0].split("=")[1];
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        v_listener.onResponse();
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Context context = getApplicationContext();
                        CharSequence text = "" + error;
                        int duration = Toast.LENGTH_SHORT;

                        Toast toast = Toast.makeText(context, text, duration);
                        toast.show();
                    }
                })
        {
            @Override
            public Map<String, String> getHeaders() {
                HashMap<String, String> headers = new HashMap<>();
                headers.put("Content-Type", "application/json");
                headers.put("Cookie", "api_token=" + apiToken);
                return headers;
            }};


        requestQueue.add(request);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_user);
        intent = getIntent();
        requestQueue = Volley.newRequestQueue(getApplicationContext());
        apiUrl = Helper.getConfigValue(getApplicationContext(), "api_url");
        apiToken = intent.getStringExtra("api_token");
        computer_id = intent.getIntExtra("computer_id", 0);
        user_id = intent.getIntExtra("user_id", 0);
        task_text = (EditText)findViewById(R.id.editText4);
        summary = (EditText)findViewById(R.id.editText5);
        b = (Button)findViewById(R.id.button3);

        b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                postTask();
            }
        });

    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        View v = getCurrentFocus();

        if (v != null &&
                (ev.getAction() == MotionEvent.ACTION_UP || ev.getAction() == MotionEvent.ACTION_MOVE) &&
                v instanceof EditText &&
                !v.getClass().getName().startsWith("android.webkit.")) {
            int scrcoords[] = new int[2];
            v.getLocationOnScreen(scrcoords);
            float x = ev.getRawX() + v.getLeft() - scrcoords[0];
            float y = ev.getRawY() + v.getTop() - scrcoords[1];

            if (x < v.getLeft() || x > v.getRight() || y < v.getTop() || y > v.getBottom())
                hideKeyboard(this);
        }
        return super.dispatchTouchEvent(ev);
    }

    public static void hideKeyboard(Activity activity) {
        if (activity != null && activity.getWindow() != null && activity.getWindow().getDecorView() != null) {
            InputMethodManager imm = (InputMethodManager)activity.getSystemService(Context.INPUT_METHOD_SERVICE);
            imm.hideSoftInputFromWindow(activity.getWindow().getDecorView().getWindowToken(), 0);
        }
    }
}
