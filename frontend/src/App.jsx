import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Results from "./pages/Results";
import About from "./pages/About";
import DisclaimerModel from "./components/DisclaimerModel";
import HowItWorks from "./pages/HowItWorks";
import WhereToBuy from "./pages/WhereToBuy";   // #Change 3

export default function App() {
  return (
    
    <BrowserRouter>
    <DisclaimerModel />

      <div className="app-shell">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/results" element={<Results />} />
            <Route path="/about" element={<About />} />
            <Route path="/where-to-buy" element={<WhereToBuy />} />   
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}