package com.dsimutin.invapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class AdminActivity extends AppCompatActivity {

    TableLayout hw_table, tasks_table;

    Intent intent;
    RequestQueue requestQueue;

    JSONObject json, tasks;

    String apiUrl = "";
    String apiToken = "";
    String computer_id;

    protected void viewTasks() throws JSONException{
        try{
            int len = tasks.names().length();
        }
        catch (NullPointerException e) {
            TableRow r = new TableRow(this);
            TextView t1 = new TextView(this);
            t1.setText("No tasks linked to this item");
            t1.setPadding(3,3,3,3);
            t1.setGravity(Gravity.CENTER);
            r.addView(t1);
            tasks_table.addView(r);
            return;
        }
        JSONArray keys = tasks.names();
        TableRow r = new TableRow(this);
        TableRow.LayoutParams params_short = new TableRow.LayoutParams(0, TableRow.LayoutParams.WRAP_CONTENT, 1f);
        TableRow.LayoutParams params_summary = new TableRow.LayoutParams(0, TableRow.LayoutParams.WRAP_CONTENT, 3f);
        TableRow.LayoutParams params_body = new TableRow.LayoutParams(0, TableRow.LayoutParams.WRAP_CONTENT, 4f);
        r.setLayoutParams(new TableRow.LayoutParams(TableRow.LayoutParams.MATCH_PARENT, TableRow.LayoutParams.WRAP_CONTENT));

        TextView t1 = new TextView(this);
        t1.setText("id");
        t1.setLayoutParams(params_short);
        t1.setPadding(3,3,3,3);
        t1.setGravity(Gravity.CENTER);
        r.addView(t1);
        TextView t2 = new TextView(this);
        t2.setLayoutParams(params_summary);
        t2.setText("Summary");
        t2.setPadding(3,3,3,3);
        t2.setGravity(Gravity.CENTER);
        r.addView(t2);
        TextView t3 = new TextView(this);
        t3.setLayoutParams(params_body);
        t3.setPadding(3,3,3,3);
        t3.setText("Task body");
        t3.setGravity(Gravity.CENTER);
        r.addView(t3);
        TextView t4 = new TextView(this);
        t4.setLayoutParams(params_short);
        t4.setPadding(3,3,3,3);
        t4.setText("uid");
        t4.setGravity(Gravity.CENTER);
        r.addView(t4);
        TextView t5 = new TextView(this);
        t5.setLayoutParams(params_short);
        t5.setText("close");
        r.addView(t5);
        tasks_table.addView(r);
        for (int i = 0; i < keys.length(); i++) {
            Log.e("TASK:", "viewTasks: " + keys.getString(i));
            String[] fields = {"summary", "body", "created_by"};
            JSONObject nested = new JSONObject(tasks.getString(keys.getString(i)));
            TableRow row = new TableRow(this);
            TextView t = new TextView(this);
            t.setLayoutParams(params_short);
            final String tid = keys.getString(i);
            t.setText(keys.getString(i));
            t.setPadding(3,3,3,3);
            t.setGravity(Gravity.CENTER);
            row.addView(t);
            for (int j = 0; j < fields.length; j++) {
                TextView v = new TextView(this);
                String text = nested.getString(fields[j]);
                if (j == 2) {
                    v.setLayoutParams(params_short);
                }
                else if (j == 0) {
                    v.setLayoutParams(params_summary);
                    text += "\n";
                }
                else if (j == 1) {
                    v.setLayoutParams(params_body);
                    text += "\n";
                }
                v.setPadding(3,3,3,3);
                v.setText(text);
                v.setGravity(Gravity.CENTER);
                row.addView(v);
            }
            Button b = new Button(this);
            b.setLayoutParams(params_short);
            b.setText("X");
            b.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    updateTaskStatus(tid, "closed");
                    TableRow t = (TableRow) v.getParent();
                    tasks_table.removeView(t);
                    if (tasks_table.getChildCount() == 1) {
                        tasks_table.removeAllViews();
                        TableRow r = new TableRow(tasks_table.getContext());
                        TextView t1 = new TextView(r.getContext());
                        t1.setText("No tasks linked to this item");
                        t1.setPadding(3,3,3,3);
                        t1.setGravity(Gravity.CENTER);
                        r.addView(t1);
                        tasks_table.addView(r);
                        return;
                    }
                }
            });
            row.addView(b);
            tasks_table.addView(row);
        }
        tasks = new JSONObject("");
    }

    private String parseJson(JSONObject j, int depth) {
        String res = "";
        Iterator<String> keys = j.keys();
        try {
            String tabs = "";
            for (int i = 0; i < depth + 1; i++) {
                tabs += "\u0009\u0009";
            }
            while (keys.hasNext()) {

                String key = keys.next();
                if (j.get(key) instanceof JSONObject) {
                    res += tabs + key + ":\n";
                    Log.e("recursive", "parseJson: " + j.get(key) +  "    " + res + "    " + key + "\n\n\n");
                    res += parseJson((JSONObject) j.get(key), depth + 1);
                } else {
                    res += tabs + key + ": " + j.get(key) + "\n";
                }
            }
        }
        catch (JSONException e) {

        }
        return res + "\n";
    }

    protected void viewAssetData() {
        JSONArray names = json.names();
        try {
            TableRow.LayoutParams params_short = new TableRow.LayoutParams(0, TableRow.LayoutParams.WRAP_CONTENT, 1f);
            TableRow.LayoutParams params_long = new TableRow.LayoutParams(0, TableRow.LayoutParams.WRAP_CONTENT, 5f);
            for (int i = 0; i < names.length(); i++) {
                TableRow r = new TableRow(this);
                TextView t = new TextView(this);
                t.setLayoutParams(params_short);
                t.setPadding(3,3,3,3);
                t.setGravity(Gravity.CENTER);
                t.setTypeface(null, Typeface.BOLD);
                t.setText(names.getString(i));
                r.addView(t);
                TextView t2 = new TextView(this);
                t2.setLayoutParams(params_long);
                t2.setPadding(3,3,3,3);
                t2.setGravity(Gravity.LEFT);
                String text = json.getString(names.getString(i));
                JSONObject jsonObject = new JSONObject(text);
                t2.setText(parseJson(jsonObject, 0));
                r.addView(t2);
                hw_table.addView(r);
            }
        }
        catch (JSONException e) {
            return;
        }

    }

    protected void updateTaskStatus(String id, String status) {
        String url = apiUrl + "/tasks";
        JSONObject payload = new JSONObject();
        try {
            payload.put("id", id);
            payload.put("status", status);
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
            }
        };
        JsonRequest request = new JsonRequest
                (Request.Method.PATCH, url, v_listener, payload, new Response.Listener<JSONObject>() {
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


    public void getTasks(final String computer_id){
        String url = apiUrl + "/tasks?computer_id=" + computer_id;
        JSONObject payload = new JSONObject();

        final VolleyResponseListener v_listener = new VolleyResponseListener() {
            @Override
            public void onError() {
                Log.e("LISTENER", "onError: FAILURE");
            }

            @Override
            public void onResponse() {
                try {
                    viewTasks();
                }
                catch (JSONException e) {
                    Log.e("LISTENER", "onError: FAILURE" + e.getStackTrace());
                }
            }
        };

        JsonRequest request = new JsonRequest
                (Request.Method.GET, url, v_listener, payload, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            tasks = response.getJSONObject("data");
                            Log.e("CONVERSION", "" + tasks.toString() );
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
        setContentView(R.layout.activity_admin);
        intent = getIntent();
        requestQueue = Volley.newRequestQueue(getApplicationContext());
        apiUrl = Helper.getConfigValue(getApplicationContext(), "api_url");
        apiToken = intent.getStringExtra("api_token");
        hw_table = (TableLayout)findViewById(R.id.hw_table);
        tasks_table = (TableLayout)findViewById(R.id.tasks_table);
        try {
            json = new JSONObject(intent.getStringExtra("data_json"));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        Log.e("PASSED", "onCreate: "+json );
        try {
            computer_id = json.getString("id");
            json.remove("id");
        } catch (JSONException e) {
            e.printStackTrace();
        }
        getTasks(computer_id);
        viewAssetData();

    }
}
