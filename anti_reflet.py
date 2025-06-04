import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Title ---
st.title("🧪 Simulation de Réflectance : Couches Minces Anti-reflets")
st.markdown("""
Cette application simule la **réflectance d'une couche mince** entre deux milieux transparents,
en fonction de la **longueur d'onde** de la lumière incidente.

Elle repose sur le principe d’interférence des ondes lumineuses réfléchies aux interfaces.
""")

# --- Explanation of the physics ---
with st.expander("📘 Explication du modèle physique"):
    st.markdown(r"""
**Hypothèses :**  
- Incidence normale  
- Milieux transparents (pas d’absorption)  
- Une seule couche mince

**Formules utilisées :**

- Coefficients de Fresnel :  
  $r_{01} = \dfrac{n_0 - n_1}{n_0 + n_1}$  
  $r_{12} = \dfrac{n_1 - n_2}{n_1 + n_2}$

- Différence de phase :  
  $\Delta = \dfrac{2 \pi n_1 d}{\lambda}$

- Réflectance totale :  
  $r = \dfrac{r_{01} + r_{12} e^{2i \Delta}}{1 + r_{01} r_{12} e^{2i \Delta}}$  
  $R = |r|^2$
""")

# --- Sidebar user inputs ---
st.sidebar.header("🎛 Paramètres du système optique")
n0 = st.sidebar.number_input("Indice du milieu incident (n₀)", value=1.0, min_value=1.0, format="%.2f")
n1 = st.sidebar.number_input("Indice de la couche mince (n₁)", value=1.38, min_value=1.0, format="%.2f")
n2 = st.sidebar.number_input("Indice du substrat (n₂)", value=1.52, min_value=1.0, format="%.2f")
d = st.sidebar.slider("Épaisseur de la couche mince (nm)", 0, 1000, 100, step=10)

# --- Convert thickness to meters ---
d_m = d * 1e-9

# --- Define wavelength range ---
wavelengths = np.linspace(400, 700, 500)  # in nanometers
wavelengths_m = wavelengths * 1e-9        # in meters

# --- Function to compute reflectance ---
def compute_reflectance(n0, n1, n2, d, wavelength):
    r01 = (n0 - n1) / (n0 + n1)
    r12 = (n1 - n2) / (n1 + n2)
    delta = (2 * np.pi * n1 * d) / wavelength
    numerator = r01 + r12 * np.exp(2j * delta)
    denominator = 1 + r01 * r12 * np.exp(2j * delta)
    r = numerator / denominator
    R = np.abs(r) ** 2
    return R

# --- Calculate reflectance ---
R = compute_reflectance(n0, n1, n2, d_m, wavelengths_m)

# --- Plot ---
fig, ax = plt.subplots()
ax.plot(wavelengths, R * 100, color='blue')
ax.set_xlabel("Longueur d'onde (nm)")
ax.set_ylabel("Réflectance (%)")
ax.set_title("Réflectance en fonction de la longueur d'onde")
ax.grid(True)
st.pyplot(fig)

# --- Observations and tips ---
st.markdown("### 📊 Observations")
st.markdown(f"""
- Épaisseur actuelle : **{d} nm**  
- La réflectance varie selon la **longueur d’onde** en raison des interférences constructives/destructives.  
- Pour un anti-reflet optimal à une longueur d'onde donnée $\lambda_0$, on utilise :  
  $d = \\dfrac{{\lambda_0}}{{4 n_1}}$
""")

# --- Footer ---
st.markdown("---")
st.markdown("🧑‍🔬 *Développé avec Streamlit pour l'étude des interférences optiques.*")
