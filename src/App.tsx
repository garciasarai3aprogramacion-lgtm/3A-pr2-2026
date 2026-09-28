import { useState } from "react";
import { Calculator, Trash2 } from "lucide-react";
import { Route, Router as WouterRouter, Switch } from "wouter";

function Home() {
  const [numero1, setNumero1] = useState("");
  const [numero2, setNumero2] = useState("");
  const [resultado, setResultado] = useState("Resultado: 0");

  const sumar = () => {
    const first = Number(numero1);
    const second = Number(numero2);

    if (
      numero1.trim() === "" ||
      numero2.trim() === "" ||
      !Number.isFinite(first) ||
      !Number.isFinite(second)
    ) {
      setResultado("Ingresa números válidos");
      return;
    }

    setResultado(`Resultado: ${first + second}`);
  };

  const limpiar = () => {
    setNumero1("");
    setNumero2("");
    setResultado("Resultado: 0");
  };

  return (
    <main className="sum-page">
      <section className="sum-card" aria-labelledby="page-title">
        <h1 id="page-title">Calculadora de Suma</h1>

        <div className="sum-form">
          <label htmlFor="numero1">Número 1</label>
          <input
            id="numero1"
            inputMode="decimal"
            value={numero1}
            onChange={(event) => setNumero1(event.target.value)}
            aria-label="Número 1"
          />

          <label htmlFor="numero2">Número 2</label>
          <input
            id="numero2"
            inputMode="decimal"
            value={numero2}
            onChange={(event) => setNumero2(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") sumar();
            }}
            aria-label="Número 2"
          />
        </div>

        <div className="sum-actions">
          <button type="button" className="sum-button sum-button-primary" onClick={sumar}>
            <Calculator size={16} />
            SUMAR
          </button>
          <button type="button" className="sum-button sum-button-secondary" onClick={limpiar}>
            <Trash2 size={16} />
            LIMPIAR
          </button>
        </div>

        <div className="sum-result" role="status">
          {resultado}
        </div>
      </section>
    </main>
  );
}

function App() {
  return (
    <WouterRouter base={import.meta.env.BASE_URL.replace(/\/$/, "")}>
      <Switch>
        <Route path="/" component={Home} />
      </Switch>
    </WouterRouter>
  );
}

export default App;