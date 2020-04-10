package com.dsimutin.invapp;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;

import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


public class MainActivity extends Activity  {
    Button b1, b2;
    EditText ed1, ed2;
    String apiUrl = "";
    String apiToken = "";
    String user_id = "";
    String access_level = "";

    RequestQueue requestQueue;

    public void moveToScan(){
        Log.e("FINAL", "" + access_level + "" +  apiToken + "" +  user_id);
        if (access_level != "" && user_id != "") {
            Intent myIntent = new Intent(getBaseContext(),   scanActivity.class);
            myIntent.putExtra("access_level", access_level);
            myIntent.putExtra("api_token", apiToken);
            myIntent.putExtra("user_id", user_id);
            startActivity(myIntent);
        }
    }

    public void getApiToken(){
        String url = apiUrl + "/auth";
        JSONObject payload = new JSONObject();
        try {
            payload.put("login", ed1.getText());
            payload.put("password", ed2.getText());
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
                Log.e("TOKEN", "getApiToken: " + apiToken);
                getAccessLevel();
                Log.e("TOKEN", "RETURNED");
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
                });
        requestQueue.add(request);
    }

    public void getAccessLevel(){
        String url = apiUrl + "/validate_token";
        Log.e("GAL", "getAccessLevel: " + apiToken);
        JSONObject payload = new JSONObject();
        try {
            payload.put("Set-Cookie", "api_token="+apiToken);
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
                moveToScan();
            }
        };
        JsonRequest request = new JsonRequest
                (Request.Method.GET, url, v_listener, payload, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        JSONObject data = new JSONObject();
                        try {
                            data = response.getJSONObject("data");

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        try {
                            String str = data.getString("access_level");
                            access_level = str;
                            str = data.getString("user_id");
                            user_id = str;
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        v_listener.onResponse();
                    }
                }, new Response.ErrorListener() {

                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Context context = getApplicationContext();
                        CharSequence text = ""+error;
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
        apiUrl = Helper.getConfigValue(getApplicationContext(), "api_url");
        requestQueue = Volley.newRequestQueue(getApplicationContext());
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        b1 = (Button)findViewById(R.id.button);
        ed1 = (EditText)findViewById(R.id.editText);
        ed2 = (EditText)findViewById(R.id.editText2);
        b2 = (Button)findViewById(R.id.button2);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                getApiToken();
            }
        });

        b2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }
}