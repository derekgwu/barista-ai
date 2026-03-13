// components/Navbar.js
import styles from "./Navbar.module.css"
import Link from "next/link"
import { SiBuymeacoffee } from "react-icons/si";

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <Link href="/" className={styles.brand}>
        <SiBuymeacoffee/>
        <span className={styles.brandName}>Cappuccino.<span className={styles.brandAi}>ai</span></span>
      </Link>

      <div className={styles.links}>
        <Link href="/prep" className={styles.navLink}>Prep</Link>
        <Link href="/schedule" className={styles.navLink}>Schedule</Link>
        <button className={styles.loginBtn}>Login</button>
      </div>
    </nav>
  )
}