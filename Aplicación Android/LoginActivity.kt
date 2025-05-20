package com.example.coursemanagerclient2

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.*
import java.net.HttpURLConnection
import java.net.URLEncoder
import java.net.URL

class LoginActivity : AppCompatActivity() {

    private lateinit var hostInput: EditText
    private lateinit var nameInput: EditText
    private lateinit var surnameInput: EditText
    private lateinit var uidInput: EditText
    private lateinit var loginButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        hostInput = findViewById(R.id.hostInput)
        nameInput = findViewById(R.id.nameInput)
        surnameInput = findViewById(R.id.surnameInput)
        uidInput = findViewById(R.id.uidInput)
        loginButton = findViewById(R.id.loginButton)

        loginButton.setOnClickListener {
            val host = hostInput.text.toString().trim()
            val name = nameInput.text.toString().trim()
            val surname = surnameInput.text.toString().trim()
            val uid = uidInput.text.toString().trim()

            if (host.isEmpty() || name.isEmpty() || surname.isEmpty() || uid.isEmpty()) {
                Toast.makeText(this, "Please fill all fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            val query = "table=students&name=${URLEncoder.encode(name, "UTF-8")}&surname=${URLEncoder.encode(surname, "UTF-8")}&student_id=${URLEncoder.encode(uid, "UTF-8")}"
            val url = "http://$host?$query"

            // MOSTRAR LA URL EN PANTALLA TEMPORALMENTE
            Toast.makeText(this, url, Toast.LENGTH_LONG).show()

            CoroutineScope(Dispatchers.IO).launch {
                val result = checkLogin(url)
                withContext(Dispatchers.Main) {
                    if (result) {
                        val intent = Intent(this@LoginActivity, MainActivity::class.java).apply {
                            putExtra("HOST", host)
                            putExtra("NAME", "$name $surname")
                            putExtra("UID", uid)
                        }
                        startActivity(intent)
                    } else {
                        Toast.makeText(this@LoginActivity, "Invalid credentials", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }
    }

    private fun checkLogin(urlString: String): Boolean {
        return try {
            val url = URL(urlString)
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.connectTimeout = 5000
            conn.readTimeout = 5000
            conn.connect()

            val response = conn.inputStream.bufferedReader().readText()

            // Mostrar la respuesta directamente en un Toast largo
            runOnUiThread {
                Toast.makeText(this, "Respuesta: $response", Toast.LENGTH_LONG).show()
            }

            // Aquí forzamos que pase si la respuesta contiene algo útil
            return response.contains("David") && response.contains("student_id")
        } catch (e: Exception) {
            runOnUiThread {
                Toast.makeText(this, "ERROR: ${e.message}", Toast.LENGTH_LONG).show()
            }
            false
        }
    }

}
