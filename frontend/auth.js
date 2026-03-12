import { auth } from "./firebase-config.js";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

// ── SIGN UP ──────────────────────────────────────────────
export async function signUp(email, password) {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;
    console.log("Signed up:", user.email);
    return user;
  } catch (error) {
    throw new Error(friendlyError(error.code));
  }
}

// ── LOGIN ─────────────────────────────────────────────────
export async function login(email, password) {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;
    console.log("Logged in:", user.email);
    return user;
  } catch (error) {
    throw new Error(friendlyError(error.code));
  }
}

// ── LOGOUT ────────────────────────────────────────────────
export async function logout() {
  await signOut(auth);
  window.location.href = "/login.html";
}

// ── GET TOKEN (send this to your Python backend) ──────────
export async function getToken() {
  const user = auth.currentUser;
  if (!user) return null;
  return await user.getIdToken();
}

// ── CALL YOUR BACKEND WITH AUTH ───────────────────────────
export async function fetchProtected(url) {
  const token = await getToken();
  const response = await fetch(url, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });
  return response.json();
}

// ── WATCH AUTH STATE ──────────────────────────────────────
export function watchAuth(callback) {
  onAuthStateChanged(auth, callback);
}

// ── FRIENDLY ERROR MESSAGES ───────────────────────────────
function friendlyError(code) {
  const messages = {
    "auth/email-already-in-use": "An account with this email already exists.",
    "auth/invalid-email": "Please enter a valid email address.",
    "auth/weak-password": "Password must be at least 6 characters.",
    "auth/user-not-found": "No account found with this email.",
    "auth/wrong-password": "Incorrect password.",
    "auth/too-many-requests": "Too many attempts. Try again later.",
  };
  return messages[code] || "Something went wrong. Please try again.";
}