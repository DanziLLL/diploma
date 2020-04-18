package com.dsimutin.invapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;


import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.Volley;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class scanActivity extends AppCompatActivity implements View.OnClickListener {
    String apiUrl = "";
    String apiToken = "";
    int computer_id;
    String data_json = "";
    private Button scanBtn;
    Intent intent;
    RequestQueue requestQueue;

    public void moveToAnother() {
        Intent myIntent = new Intent();
        myIntent.putExtra("computer_id", computer_id);
        myIntent.putExtra("access_level", intent.getStringExtra("access_level"));
        myIntent.putExtra("api_token", apiToken);
        myIntent.putExtra("user_id", intent.getStringExtra("user_id"));
        Log.e("FINAL", "onActivityResult: "+data_json );
        myIntent.putExtra("data_json", data_json);
        if (intent.getStringExtra("access_level").equals("user")) {
            moveToUser(myIntent);
        }
        if (intent.getStringExtra("access_level").equals("admin")) {
            moveToAdmin(myIntent);
        }
    }

    public void getAssetId(final String inventory_id){
        String url = apiUrl + "/computer?inventory_id=" + inventory_id;
        JSONObject payload = new JSONObject();

        final VolleyResponseListener v_listener = new VolleyResponseListener() {
            @Override
            public void onError() {
                Log.e("LISTENER", "onError: FAILURE");
            }

            @Override
            public void onResponse() {
                moveToAnother();
            }
        };

        JsonRequest request = new JsonRequest
                (Request.Method.GET, url, v_listener, payload, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        JSONObject data = new JSONObject();
                        String str = "";
                        try {
                            data = response.getJSONObject("data");
                            data_json = data.toString();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        try {
                            computer_id = Integer.parseInt(data.getString("id"));
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
                headers.put("Cookie", "api_token=" + apiToken);
                return headers;
            }
            };
        requestQueue.add(request);
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_scan);
        intent = getIntent();
        scanBtn = (Button)findViewById(R.id.scan_button);
        scanBtn.setOnClickListener(this);
        requestQueue = Volley.newRequestQueue(getApplicationContext());
        apiUrl = Helper.getConfigValue(getApplicationContext(), "api_url");
        apiToken = intent.getStringExtra("api_token");
    }

    public void onClick(View v){
        if(v.getId()==R.id.scan_button){
            IntentIntegrator scanIntegrator = new IntentIntegrator(this);
            scanIntegrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE_TYPES);
            scanIntegrator.setPrompt("");
            scanIntegrator.setOrientationLocked(true);
            scanIntegrator.initiateScan();
        }
    }

    public void moveToUser(Intent myIntent){
        myIntent.setClass(getBaseContext(), UserActivity.class);
        startActivity(myIntent);
    }

    public void moveToAdmin(Intent myIntent){
        myIntent.setClass(getBaseContext(), AdminActivity.class);
        startActivity(myIntent);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        IntentResult scanningResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        Log.e("ONACTIVITYRESULT", "onResponse: " + data_json );
        if (scanningResult != null) {
            String scanContent = scanningResult.getContents();
            if (!scanContent.substring(0, 7).equals("invapp_")) {
                Toast toast = Toast.makeText(getApplicationContext(),
                        "Not a valid inventory_app QR code", Toast.LENGTH_SHORT);
                toast.show();
            }
            else {
                getAssetId(scanContent);
            }
        }
        else{
            Toast toast = Toast.makeText(getApplicationContext(),
                    "No scan data received!", Toast.LENGTH_SHORT);
            toast.show();
        }
    }
}
