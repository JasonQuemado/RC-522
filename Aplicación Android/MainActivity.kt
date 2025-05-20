package com.example.coursemanagerclient2

import android.content.Intent
import android.os.Bundle
import android.view.Gravity
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.*
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL
import java.time.DayOfWeek
import java.time.LocalDate
import java.time.LocalTime
import java.util.*

class MainActivity : AppCompatActivity() {

    private lateinit var host: String
    private lateinit var name: String
    private lateinit var uid: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        host = intent.getStringExtra("HOST") ?: ""
        name = intent.getStringExtra("NAME") ?: ""
        uid = intent.getStringExtra("UID") ?: ""

        val welcomeText = findViewById<TextView>(R.id.welcomeText)
        val logoutButton = findViewById<Button>(R.id.logoutButton)
        val queryInput = findViewById<EditText>(R.id.queryInput)
        val sendButton = findViewById<Button>(R.id.sendButton)
        val resultTable = findViewById<TableLayout>(R.id.resultTable)

        welcomeText.text = "Welcome, $name"

        logoutButton.setOnClickListener {
            val intent = Intent(this, LoginActivity::class.java)
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(intent)
            finish()
        }

        sendButton.setOnClickListener {
            val table = queryInput.text.toString().trim()
            if (table.isEmpty()) {
                Toast.makeText(this, "Please enter a query (e.g. tasks)", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val fullUrl = "http://$host?table=$table&student_id=$uid"
            resultTable.removeAllViews()

            CoroutineScope(Dispatchers.IO).launch {
                val rows = fetchData(fullUrl, table)
                withContext(Dispatchers.Main) {
                    when (table) {
                        "timetables" -> displayTable(resultTable, rows, listOf("day", "hour", "subject", "room"))
                        "tasks" -> displayTable(resultTable, rows, listOf("date", "subject", "name"))
                        "marks" -> displayTable(resultTable, rows, listOf("subject", "name", "mark"))
                        else -> displayRawText(resultTable, rows, table)
                    }
                }
            }
        }
    }

    private fun fetchData(urlString: String, table: String): List<JSONObject> {
        return try {
            val url = URL(urlString)
            val conn = url.openConnection() as HttpURLConnection
            conn.connectTimeout = 5000
            conn.readTimeout = 5000
            conn.requestMethod = "GET"
            conn.connect()

            val rawJson = conn.inputStream.bufferedReader().readText()
            val jsonArray = JSONArray(rawJson)
            if (jsonArray.length() == 0) return emptyList()

            if (table == "timetables") {
                sortTimetablesByCurrentDay(jsonArray)
            } else {
                (0 until jsonArray.length()).map { jsonArray.getJSONObject(it) }
            }
        } catch (e: Exception) {
            listOf(JSONObject().put("error", e.message ?: "Unknown error"))
        }
    }

    private fun displayTable(tableLayout: TableLayout, data: List<JSONObject>, columns: List<String>) {
        val headerRow = TableRow(this)
        columns.forEach { title ->
            val tv = TextView(this)
            tv.text = title.replaceFirstChar { it.uppercaseChar() }
            tv.setPadding(8, 8, 8, 8)
            tv.gravity = Gravity.CENTER
            tv.setTypeface(null, android.graphics.Typeface.BOLD)
            headerRow.addView(tv)
        }
        tableLayout.addView(headerRow)

        for (obj in data) {
            val row = TableRow(this)
            columns.forEach { col ->
                val tv = TextView(this)
                tv.text = obj.optString(col, "")
                tv.setPadding(8, 8, 8, 8)
                tv.gravity = Gravity.CENTER
                row.addView(tv)
            }
            tableLayout.addView(row)
        }
    }

    private fun displayRawText(tableLayout: TableLayout, data: List<JSONObject>, table: String) {
        val tv = TextView(this)
        tv.setPadding(16, 16, 16, 16)
        val builder = StringBuilder()
        builder.append("=== $table ===\n\n")
        for (obj in data) {
            builder.append(obj.toString()).append("\n\n")
        }
        tv.text = builder.toString()
        tableLayout.addView(tv)
    }

    private fun sortTimetablesByCurrentDay(array: JSONArray): List<JSONObject> {
        val today = LocalDate.now().dayOfWeek  // ej. DayOfWeek.THURSDAY
        val dayCodes = listOf("Mon", "Tue", "Wed", "Thu", "Fri")
        val codeToDay = mapOf(
            "Mon" to DayOfWeek.MONDAY,
            "Tue" to DayOfWeek.TUESDAY,
            "Wed" to DayOfWeek.WEDNESDAY,
            "Thu" to DayOfWeek.THURSDAY,
            "Fri" to DayOfWeek.FRIDAY
        )

        fun dayDistance(code: String): Int {
            val day = codeToDay[code] ?: return 99
            val diff = day.value - today.value
            return if (diff >= 0) diff else diff + 7
        }

        return (0 until array.length())
            .map { array.getJSONObject(it) }
            .sortedWith(compareBy({ dayDistance(it.getString("day")) }, { LocalTime.parse(it.getString("hour")) }))
    }
}
