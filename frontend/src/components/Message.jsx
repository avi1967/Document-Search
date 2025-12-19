export default function Message({ role, text }) {
  return (
    <div className={role === "user" ? "user" : "bot"}>
      {text}
    </div>
  );
}
