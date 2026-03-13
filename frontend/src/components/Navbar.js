// components/Navbar.js
import styles from "./Navbar.module.css"
import Link from "next/link"

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <Link href="/" className={styles.brand}>
        <span className={styles.brandIcon}>☕</span>
        <span className={styles.brandName}>Cappuccino<span className={styles.brandAi}>AI</span></span>
      </Link>

      <div className={styles.links}>
        <Link href="/prep" className={styles.navLink}>Prep</Link>
        <Link href="/schedule" className={styles.navLink}>Schedule</Link>
        <button className={styles.loginBtn}>Login</button>
      </div>
    </nav>
  )
}