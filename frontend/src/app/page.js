// app/page.js
import Link from "next/link"
import styles from "./page.module.css"
import Navbar from "@/components/Navbar"
import { SiBuymeacoffee } from "react-icons/si";

export default function Home() {
  return (
    <>
    <Navbar/>
    <main className={styles.main}>
      <div className={styles.hero}>
        <p className={styles.eyebrow}>Your networking co-pilot</p>
        <h1 className={styles.title}>
          Cappuccino.<span className={styles.titleAccent}>ai</span>
        </h1>
        <p className={styles.subtitle}>
          Walk into every coffee chat prepared, confident, and ready to impress.
        </p>
      </div>

      <div className={styles.cards}>
        <div className={styles.card}>
          <div className={styles.cardIcon}>☕</div>
          <h2 className={styles.cardTitle}>Meet Your Barista Agent</h2>
          <p className={styles.cardDesc}>
            Tell your Barista your company and dream role. It researches
            culture, the job, and recent news — then brews a personalized
            prep doc so you walk in confident.
          </p>
          <Link href="/prep" className={styles.cardBtn}>
            Meet your Barista
          </Link>
        </div>

        <div className={styles.card}>
          <div className={styles.cardIcon}>📅</div>
          <h2 className={styles.cardTitle}>Schedule a Coffee Chat</h2>
          <p className={styles.cardDesc}>
            Upload your resume, pick a time, and we'll create a Zoom link,
            book the calendar, and prep both sides for a great conversation.
          </p>
          <Link href="/schedule" className={styles.cardBtnSecondary}>
            Book a chat
          </Link>
        </div>
      </div>
    </main>
    </>
  )
}