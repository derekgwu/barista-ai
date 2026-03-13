// app/prep/page.js
"use client"
import { useState, useRef } from "react"
import Navbar from "../../components/Navbar"
import styles from "./prep.module.css"

export default function PrepPage() {
  const [form, setForm] = useState({ company: "", jobTitle: "", background: "" })
  const [resume, setResume] = useState(null)
  const [result, setResult] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const fileRef = useRef()

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function handleFile(e) {
    const file = e.target.files[0]
    if (file) setResume(file)
  }

  async function handleSubmit() {
    if (!form.company || !form.jobTitle) {
      setError("Company and job title are required.")
      return
    }
    setError("")
    setLoading(true)
    setResult("")

    const body = new FormData()
    body.append("company", form.company)
    body.append("job_title", form.jobTitle)
    body.append("background", form.background)
    if (resume) body.append("resume", resume)

    try {
      const res = await fetch("http://localhost:8000/prep", {
        method: "POST",
        body,
      })
      const data = await res.json()
      setResult(data.result || data.error)
    } catch (err) {
      setError("Could not connect to backend. Make sure the server is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Navbar />
      <main className={styles.main}>
        <div className={styles.container}>

          <div className={styles.header}>
            <span className={styles.tag}>Barista Agent</span>
            <h1 className={styles.title}>Brew your prep doc</h1>
            <p className={styles.subtitle}>
              Enter your target company and role. Your Barista will research
              culture, the job, and recent news — then craft a personalized
              prep document for your networking call.
            </p>
          </div>

          <div className={styles.form}>
            <div className={styles.row}>
              <div className={styles.field}>
                <label className={styles.label}>Company *</label>
                <input
                  name="company"
                  placeholder="e.g. Stripe"
                  className={styles.input}
                  value={form.company}
                  onChange={handleChange}
                />
              </div>
              <div className={styles.field}>
                <label className={styles.label}>Job title *</label>
                <input
                  name="jobTitle"
                  placeholder="e.g. Solutions Architect"
                  className={styles.input}
                  value={form.jobTitle}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Your background <span className={styles.optional}>(optional)</span></label>
              <textarea
                name="background"
                placeholder="e.g. CS junior, did a fintech internship, interested in breaking into PM..."
                className={styles.textarea}
                value={form.background}
                onChange={handleChange}
              />
            </div>

            <div className={styles.field}>
              <label className={styles.label}>Resume <span className={styles.optional}>(optional)</span></label>
              <div
                className={styles.fileZone}
                onClick={() => fileRef.current.click()}
              >
                <input
                  ref={fileRef}
                  type="file"
                  accept=".pdf,.docx"
                  className={styles.fileInput}
                  onChange={handleFile}
                />
                {resume ? (
                  <p className={styles.fileName}>📄 {resume.name}</p>
                ) : (
                  <p className={styles.filePlaceholder}>
                    Click to upload PDF or DOCX
                  </p>
                )}
              </div>
            </div>

            {error && <p className={styles.error}>{error}</p>}

            <button
              className={styles.btn}
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? (
                <span className={styles.btnLoading}>
                  <span className={styles.spinner} /> Brewing your prep doc...
                </span>
              ) : (
                "☕ Brew my prep doc"
              )}
            </button>
          </div>

          {result && (
            <div className={styles.result}>
              <div className={styles.resultHeader}>
                <span className={styles.resultTag}>Your prep doc</span>
                <h2 className={styles.resultTitle}>
                  {form.jobTitle} at {form.company}
                </h2>
              </div>
              <div className={styles.resultBody}>
                {result.split("\n").map((line, i) => {
                  if (line.startsWith("## ")) return <h3 key={i} className={styles.resultH}>{line.replace("## ", "")}</h3>
                  if (line.startsWith("**") && line.endsWith("**")) return <p key={i} className={styles.resultBold}>{line.replaceAll("**", "")}</p>
                  if (line.trim() === "") return <div key={i} className={styles.resultSpacer} />
                  return <p key={i} className={styles.resultP}>{line}</p>
                })}
              </div>
            </div>
          )}

        </div>
      </main>
    </>
  )
}