"""Fictional product-document content for Northfield Lab Supply.

Every fact lives in a data dict here so the same value appears identically in
the manual, spec sheet and technical note of a product. Builders return a list
of blocks: ("h2", text), ("p", text), ("ul", [items]), ("ol", [items]),
("table", header, rows).
"""

CONTACT = "customerservice@northfieldlabsupply.example"
WARRANTY_NOTE = ("Warranty claims: contact Customer service with the order number and a description of the fault. "
                 "The warranty covers manufacturing defects and does not cover damage from misuse, spills or unauthorised repair.")

# ---------------------------------------------------------------- equipment data
MC12 = dict(
    name="MC-12 microcentrifuge",
    intro=("The MC-12 is a compact benchtop microcentrifuge for 1.5 ml and 2.0 ml tubes. It is sold in two versions: "
           "the Standard (fixed speed settings) and the Plus (variable speed, digital display and a second rotor)."),
    versions=(["", "Standard", "Plus"], [
        ["Speed", "3 fixed settings: 4,000, 8,000, 13,000 rpm", "Variable 500 to 15,000 rpm in 100 rpm steps"],
        ["Maximum RCF", "14,200 ×g", "18,900 ×g"],
        ["Rotors supplied", "12-place (1.5/2.0 ml tubes)", "12-place (1.5/2.0 ml tubes) and 8-place PCR strip rotor"],
        ["Display and timer", "None; run continuously or short-spin", "Digital speed and timer display; 10 s to 99 min or continuous"],
        ["Warranty", "1 year", "2 years"]]),
    safety=["Place the unit on a level, stable surface with at least 10 cm clearance on all sides.",
            "Never run the centrifuge with an unbalanced load or with the lid open. The lid lock and imbalance cut-out are safety devices, not operating controls.",
            "Do not use tubes that are cracked, deformed or rated below the maximum RCF of your version.",
            "Do not spin flammable, explosive or hazardous biological material unless you have assessed the risk.",
            "Unplug the unit before cleaning or moving it."],
    setup=["Remove the packaging and check the contents against the packing list: centrifuge unit, rotor(s), mains cable (UK plug) and this manual.",
           "Place the unit on a level surface and connect the mains cable (230 V AC, 50 Hz).",
           "Fit the rotor by pressing it onto the drive spindle until it seats, then tighten the rotor nut by hand.",
           "Run the unit empty at the lowest speed for 10 seconds to confirm it runs smoothly."],
    operation=["Load an even number of tubes in opposite positions. For an odd number, balance with a tube of the same type and the same volume of water.",
               "Close the lid until it latches.",
               "Standard: choose one of the three speed settings, then press Start to run continuously, or hold Short spin for a brief run. Plus: set the speed and the time on the display, then press Start.",
               "Wait until the rotor has stopped completely before opening the lid. Braking takes about 15 seconds.",
               "Remove the tubes carefully and switch off at the mains."],
    maintenance=["Wipe the chamber and rotor with a damp cloth and mild detergent after use. Dry before closing the lid.",
                 "Do not autoclave the rotor. Inspect it monthly for cracks or corrosion and replace it if damaged.",
                 "Clean spills immediately; disinfect with 70 % ethanol if biological material has spilled."],
    trouble=[["Does not start", "Lid not latched; mains cable not connected", "Close the lid until it clicks; check the cable and socket"],
             ["Loud vibration", "Unbalanced tubes", "Stop the run, check the tubes are balanced and opposite each other"],
             ["Stops early or shows an error (Plus)", "Imbalance cut-out triggered", "Rebalance the load and restart"],
             ["Rotor does not seat", "Spindle dirty", "Clean the spindle and rotor bore and refit"]],
    warranty="Standard: 1 year. Plus: 2 years.",
)
MC12_SPEC = {
    "Standard": [["Rotor", "12-place, for 1.5 ml and 2.0 ml tubes"], ["Speed settings", "4,000, 8,000 and 13,000 rpm (fixed)"],
        ["Maximum RCF", "14,200 ×g at 13,000 rpm"], ["Rotor radius", "7.5 cm"], ["Run time", "Continuous, or short spin while the button is held"],
        ["Acceleration / braking", "About 10 s / about 15 s"], ["Noise", "Below 58 dB(A) at 13,000 rpm"], ["Safety", "Lid lock and imbalance cut-out"],
        ["Power", "230 V AC, 50 Hz, 90 W"], ["Dimensions (W × D × H)", "24 × 28 × 15 cm"], ["Weight", "3.2 kg"],
        ["Operating conditions", "5 to 40 °C, 20 to 80 % humidity, non-condensing"], ["Supplied with", "Unit, 12-place rotor, mains cable (UK plug), user manual"], ["Warranty", "1 year"]],
    "Plus": [["Rotors", "12-place (1.5 ml and 2.0 ml tubes) and 8-place PCR strip rotor"], ["Speed", "500 to 15,000 rpm in 100 rpm steps"],
        ["Maximum RCF", "18,900 ×g at 15,000 rpm"], ["Rotor radius (12-place)", "7.5 cm"], ["Display", "Digital speed (rpm or ×g) and timer"], ["Run time", "10 s to 99 min, or continuous"],
        ["Acceleration / braking", "About 8 s / about 15 s"], ["Noise", "Below 60 dB(A) at 15,000 rpm"], ["Safety", "Lid lock and imbalance cut-out"],
        ["Power", "230 V AC, 50 Hz, 120 W"], ["Dimensions (W × D × H)", "24 × 28 × 16 cm"], ["Weight", "3.6 kg"],
        ["Operating conditions", "5 to 40 °C, 20 to 80 % humidity, non-condensing"], ["Supplied with", "Unit, both rotors, mains cable (UK plug), user manual"], ["Warranty", "2 years"]],
}
MC12_TECH = [
    ("Purpose", ["This note explains which tubes and rotors can be used together, and how to balance a load. It applies to both the Standard and the Plus unless stated."]),
    ("Compatible tubes", [("ul", ["12-place rotor (both versions): 1.5 ml and 2.0 ml snap-cap tubes, including Northfield microcentrifuge tubes 1.5 ml (rated to 20,000 ×g).",
                                  "8-place PCR strip rotor (Plus only): 0.2 ml tube strips. This rotor is not available for the Standard.",
                                  "Tubes must be rated for at least the maximum RCF of your version: 14,200 ×g (Standard) or 18,900 ×g (Plus)."])]),
    ("Balancing", [("ol", ["Load tubes in opposite positions.", "For an odd number of tubes, add a balance tube of the same type with the same volume of water.",
                           "Check that liquid volumes in opposite tubes differ by no more than 0.1 ml."])]),
    ("Speed and RCF", ["RCF depends on speed and rotor radius: RCF = 1.118 × 10^-5 × radius (cm) × rpm². For the 12-place rotor (7.5 cm) this gives 1,300 ×g at 4,000 rpm, 5,400 ×g at 8,000 rpm and 14,200 ×g at 13,000 rpm."]),
    ("Not covered", ["Use with tubes larger than 2.0 ml, or with adapters not supplied by Northfield, is not covered by this note."]),
]
MC10 = dict(
    name="MC-10 microcentrifuge",
    intro="The MC-10 Basic is a discontinued benchtop microcentrifuge with a 10-place rotor for 1.5 ml tubes and one fixed speed. It has been replaced by the MC-12 Standard.",
    versions=None,
    safety=["Place the unit on a level, stable surface.", "Never run with an unbalanced load or with the lid open.", "Unplug before cleaning or moving."],
    setup=["Check the contents: unit, 10-place rotor, mains cable (UK plug).", "Connect the mains cable (230 V AC, 50 Hz).", "Fit the rotor and tighten the nut by hand."],
    operation=["Load tubes in opposite positions and balance odd numbers with a water-filled tube.", "Close the lid and press Start. The unit runs at 12,000 rpm (10,800 ×g).",
               "Wait for the rotor to stop before opening the lid."],
    maintenance=["Wipe with a damp cloth and mild detergent. Do not autoclave the rotor."],
    trouble=[["Does not start", "Lid not latched", "Close the lid until it clicks"], ["Vibration", "Unbalanced tubes", "Rebalance the tubes"]],
    warranty="1 year.",
)
AB220 = dict(
    name="AB-220 analytical balance",
    intro=("The AB-220 is an analytical balance with a capacity of 220 g and a readability of 0.1 mg. It is sold in two versions: "
           "the Standard and the Certified, which is supplied with a calibration certificate and a longer warranty."),
    versions=(["", "Standard", "Certified"], [
        ["Calibration certificate", "Not included", "Included (issued with the unit)"],
        ["Warranty", "1 year", "2 years"],
        ["Availability", "In stock", "Made to order (about 3 working days)"]]),
)
AB220_R3 = dict(warm=30, cal_weight="200 g", temp="15 to 30 °C", rev="R3")
AB220_R2 = dict(warm=15, cal_weight="100 g", temp="10 to 35 °C", rev="R2")
HB2 = dict(
    name="HB-2 dry block heater",
    intro=("The HB-2 is a digital dry block heater with interchangeable blocks. It is sold in two versions: "
           "the Single block and the Dual block, which has two independently controlled blocks."),
    versions=(["", "Single block", "Dual block"], [
        ["Blocks", "One block for 20 × 1.5 ml tubes", "Two blocks, each for 20 × 1.5 ml tubes"],
        ["Temperature control", "One", "Two, independent"],
        ["Power", "150 W", "280 W"], ["Warranty", "1 year", "2 years"]]),
)
VM10 = dict(
    name="VM-10 vortex mixer",
    intro=("The VM-10 is a benchtop vortex mixer with a cup head. It is sold in two versions: the Basic (fixed speed) and the Variable speed "
           "(adjustable speed with touch and continuous modes)."),
    versions=(["", "Basic", "Variable speed"], [
        ["Speed", "Fixed, 2,800 rpm", "Adjustable, 200 to 3,000 rpm"],
        ["Modes", "Continuous (on/off switch)", "Touch and continuous"],
        ["Power", "50 W", "60 W"], ["Warranty", "1 year", "2 years"]]),
)

# ---------------------------------------------------------------- consumables data
CONS = {
 "PT200": dict(name="Filter pipette tips 200 µl", rows=[["Product", "Filter pipette tips, 200 µl"], ["Fits", "Universal fit, single-channel pipettes of 20 to 200 µl"],
     ["Material", "Polypropylene tip; polyethylene filter"], ["Length", "53 mm"], ["Filter", "Aerosol-barrier filter"], ["Sterility", "Sterile (gamma irradiation, SAL 10^-6)"],
     ["Free from", "DNase, RNase and pyrogens"], ["Packaging", "Racks of 96 tips"], ["Pack sizes", "Box of 960 (10 racks of 96); case of 5 boxes (4,800 tips)"],
     ["Storage", "Room temperature, dry, away from direct sunlight"], ["Shelf life", "5 years from manufacture"]],
     coa=[["Sterility", "Pass"], ["DNase", "Not detected"], ["RNase", "Not detected"], ["Pyrogens (endotoxin)", "Below 0.01 EU/ml"], ["Filter integrity", "Pass"]]),
 "MT15": dict(name="Microcentrifuge tubes 1.5 ml", rows=[["Product", "Microcentrifuge tubes, 1.5 ml"], ["Material", "Clear polypropylene"], ["Closure", "Attached snap cap"],
     ["Graduation", "Printed graduations and writing area"], ["Sterility", "Non-sterile"], ["Maximum RCF", "20,000 ×g"], ["Temperature range", "-80 to 100 °C"],
     ["Pack sizes", "Bag of 500; case of 10 bags (5,000 tubes)"], ["Storage", "Room temperature, dry"]]),
 "CT50": dict(name="Conical centrifuge tubes 50 ml", rows=[["Product", "Conical centrifuge tubes, 50 ml"], ["Material", "Polypropylene"], ["Closure", "Screw cap"],
     ["Graduation", "5 ml steps, with writing area"], ["Sterility", "Sterile (gamma irradiation)"], ["Maximum RCF", "12,500 ×g"], ["Pack size", "Pack of 25 sterile tubes"],
     ["Storage", "Room temperature, dry"]],
     coa=[["Sterility", "Pass"], ["Leak test (cap closed, inverted)", "Pass"], ["Maximum RCF test, 12,500 ×g", "Pass"]]),
 "GL": dict(name="Nitrile examination gloves, powder-free", rows=[["Product", "Nitrile examination gloves, powder-free"], ["Size", "Medium (other sizes are not currently offered)"],
     ["Material", "Nitrile"], ["Fit", "Ambidextrous"], ["Palm thickness", "0.10 mm (typical)"], ["Length", "240 mm (minimum)"], ["Sterility", "Non-sterile"],
     ["Standards", "EN 455 parts 1 to 3; EN ISO 374-1"], ["Pack size", "Box of 100"], ["Storage", "Cool, dry, away from direct sunlight"]]),
 "SC60": dict(name="Specimen containers 60 ml", rows=[["Product", "Specimen containers, 60 ml"], ["Material", "Polypropylene"], ["Closure", "Screw cap with leak-resistant seal"],
     ["Opening", "Wide mouth"], ["Graduation", "10 ml steps"], ["Sterility", "Sterile (gamma irradiation)"], ["Pack size", "Pack of 100 containers with caps"],
     ["Storage", "Room temperature, dry"]],
     coa=[["Sterility", "Pass"], ["Leak test (cap closed, inverted, 30 min)", "Pass"], ["Cap fit", "Pass"]]),
 "SP10": dict(name="Serological pipettes 10 ml", rows=[["Product", "Serological pipettes, 10 ml"], ["Material", "Polystyrene"], ["Graduation", "0.1 ml steps"],
     ["Colour code", "Orange (10 ml)"], ["Wrapping", "Individually wrapped"], ["Sterility", "Sterile (gamma irradiation)"], ["Free from", "Pyrogens"],
     ["Pack size", "Pack of 200 pipettes"], ["Storage", "Room temperature, dry"]],
     coa=[["Sterility", "Pass"], ["Pyrogens (endotoxin)", "Below 0.01 EU/ml"], ["Volume accuracy", "Within ±1 % of nominal"]]),
}

# ---------------------------------------------------------------- more equipment detail
AB220_SPEC = {
    "Standard": [["Capacity", "220 g"], ["Readability", "0.1 mg"], ["Repeatability (standard deviation)", "0.1 mg"], ["Linearity", "±0.2 mg"],
        ["Stabilisation time", "About 3 s"], ["Pan", "90 mm, stainless steel"], ["Draft shield", "Glass, three doors"], ["Units", "g, mg, ct"],
        ["Calibration", "External, with a 200 g test weight (not supplied)"], ["Warm-up", "30 minutes"], ["Power", "12 V DC adaptor (UK plug)"],
        ["Dimensions (W × D × H)", "21 × 34 × 32 cm"], ["Weight", "5.2 kg"], ["Operating conditions", "15 to 30 °C, 20 to 80 % humidity, non-condensing"],
        ["Supplied with", "Balance, draft shield, mains adaptor (UK plug), user manual"], ["Warranty", "1 year"]],
    "Certified": [["Capacity", "220 g"], ["Readability", "0.1 mg"], ["Repeatability (standard deviation)", "0.1 mg"], ["Linearity", "±0.2 mg"],
        ["Stabilisation time", "About 3 s"], ["Pan", "90 mm, stainless steel"], ["Draft shield", "Glass, three doors"], ["Units", "g, mg, ct"],
        ["Calibration", "External, with a 200 g test weight (not supplied)"], ["Warm-up", "30 minutes"], ["Power", "12 V DC adaptor (UK plug)"],
        ["Dimensions (W × D × H)", "21 × 34 × 32 cm"], ["Weight", "5.2 kg"], ["Operating conditions", "15 to 30 °C, 20 to 80 % humidity, non-condensing"],
        ["Calibration certificate", "Supplied with the unit, traceable to national standards through the test weights used"],
        ["Supplied with", "Balance, draft shield, mains adaptor (UK plug), calibration certificate, user manual"], ["Warranty", "2 years"],
        ["Availability", "Made to order, about 3 working days"]],
}
HB2_SPEC = {
    "Single block": [["Temperature range", "Ambient +5 °C to 150 °C"], ["Setting resolution", "0.1 °C"], ["Temperature uniformity across the block", "±0.5 °C at 37 °C"],
        ["Accuracy", "±1 °C"], ["Heat-up to 100 °C", "About 20 min"], ["Timer", "1 min to 99 h 59 min"], ["Block capacity", "20 × 1.5 ml tubes"],
        ["Over-temperature cut-out", "165 °C"], ["Power", "230 V AC, 50 Hz, 150 W"], ["Dimensions (W × D × H)", "14 × 22 × 12 cm"], ["Weight", "1.8 kg"],
        ["Supplied with", "Heater unit, one block, mains cable (UK plug), user manual"], ["Warranty", "1 year"]],
    "Dual block": [["Temperature range", "Ambient +5 °C to 150 °C, each block"], ["Setting resolution", "0.1 °C"], ["Temperature uniformity across a block", "±0.5 °C at 37 °C"],
        ["Accuracy", "±1 °C"], ["Heat-up to 100 °C", "About 22 min, both blocks"], ["Timer", "1 min to 99 h 59 min, per block"], ["Block capacity", "2 × 20 × 1.5 ml tubes"],
        ["Controls", "Two independent temperature controls"], ["Over-temperature cut-out", "165 °C per block"], ["Power", "230 V AC, 50 Hz, 280 W"],
        ["Dimensions (W × D × H)", "26 × 22 × 12 cm"], ["Weight", "3.1 kg"], ["Supplied with", "Heater unit, two blocks, mains cable (UK plug), user manual"], ["Warranty", "2 years"]],
}
VM10_SPEC = {
    "Basic": [["Speed", "Fixed, 2,800 rpm"], ["Orbit", "4 mm"], ["Mode", "Continuous (on/off switch)"], ["Head", "Cup head"], ["Tube capacity", "Tubes up to 15 ml in the cup head"],
        ["Duty cycle", "30 minutes on, then 10 minutes off"], ["Power", "230 V AC, 50 Hz, 50 W"], ["Dimensions (W × D × H)", "11 × 16 × 12 cm"], ["Weight", "1.9 kg"],
        ["Supplied with", "Mixer, cup head, mains cable (UK plug), user manual"], ["Warranty", "1 year"]],
}
AB220_TECH = [
    ("Purpose", ["This note explains where to site the AB-220, how to warm it up and how to calibrate it. It applies to both versions."]),
    ("Siting", [("ul", ["Use a firm bench, away from draughts, vibration, direct sunlight and air conditioning outlets.",
                         "Operating conditions are 15 to 30 °C and 20 to 80 % humidity, non-condensing.", "Level the balance with the feet until the level indicator is centred."])]),
    ("Warm-up", ["Leave the balance powered for 30 minutes before use or calibration, so the electronics reach a stable temperature."]),
    ("Calibration routine", [("ol", ["After warm-up, press and hold the calibration key.", "Place the 200 g test weight on the centre of the pan when prompted (the weight is not supplied).",
                                    "Remove the weight when prompted and wait for the confirmation message.", "Recalibrate after moving the balance or after a large temperature change."])]),
    ("Drift", ["If readings drift, check for draughts, static charge on the sample or container, and temperature differences between the sample and the balance."]),
    ("Certified version", ["The calibration certificate supplied with the AB-220 Certified applies to that unit only. It does not replace regular calibration checks by the user."]),
]
HB2_TECH = [
    ("Purpose", ["This note explains the temperature performance of the HB-2 and how to use the blocks correctly. It applies to both versions."]),
    ("Temperature uniformity", ["Temperature uniformity across a block is ±0.5 °C at 37 °C. Allow the block to stabilise for at least 10 minutes after reaching the set point before starting a timed run."]),
    ("Heat-up", ["Heat-up to 100 °C takes about 20 minutes (Single block) or about 22 minutes with both blocks of the Dual block heating together."]),
    ("Using the blocks", [("ul", ["Each block holds 20 × 1.5 ml tubes. Seat tubes fully so they touch the bottom of the wells.", "Change blocks only when the heater is switched off and cool to the touch; no tools are needed.",
                                  "Do not use a damaged block.", "Dual block: each block has its own temperature control and timer."])]),
    ("Limits", ["The maximum temperature is 150 °C. The over-temperature cut-out operates at 165 °C and is a safety device, not an operating setting."]),
]
VM10_TECH = [
    ("Purpose", ["This note explains the operating modes of the VM-10 and which tubes can be mixed. It applies to both versions unless stated."]),
    ("Operating modes", [("ul", ["Basic: continuous operation only, using the on/off switch, at a fixed 2,800 rpm.",
                                  "Variable speed: set the speed between 200 and 3,000 rpm with the dial. Touch mode runs while the tube presses the cup head; continuous mode runs until switched off."])]),
    ("Tube compatibility", ["The cup head accommodates tubes up to 15 ml. Mixing 50 ml tubes is not recommended."]),
    ("Duty cycle", ["Run continuously for no more than 30 minutes, then rest the unit for 10 minutes."]),
    ("Good practice", [("ul", ["Hold the tube firmly and avoid overfilling; fill tubes to no more than two-thirds.", "Start at a low speed and increase gradually (Variable speed only)."])]),
]
PT_TECH = [
    ("Purpose", ["This note explains which pipettes the Northfield filter pipette tips 200 µl fit."]),
    ("Fit", ["The tips are universal-fit tips for single-channel pipettes of 20 to 200 µl with a standard conical tip cone. Press the tip on firmly and check that it seals before use."]),
    ("Not covered", ["The tips are not intended for multichannel pipettes with a non-standard cone, or for pipettes outside the 20 to 200 µl range. Northfield does not list individual pipette models; test the fit on your own pipette before routine use."]),
    ("Handling", [("ul", ["Keep tips in the rack until use to preserve sterility.", "Close the box lid after use."])]),
]
# Planted contradiction (TEST_TRAPS.md, T-14): this note says 15,000 ×g while the current datasheet
# and certificate of analysis say 12,500 ×g. Both documents are current. Do not "fix" it.
CT_TECH = [
    ("Purpose", ["This note explains how to use the Northfield conical centrifuge tubes 50 ml in a centrifuge."]),
    ("Rotors", ["Use the tubes in fixed-angle or swing-bucket rotors with buckets or adapters designed for 50 ml conical tubes."]),
    ("Centrifugal limit", ["The tubes are rated to 15,000 ×g with the cap closed."]),
    ("Filling", [("ul", ["Fill to no more than the 50 ml graduation.", "Close the screw cap fully before centrifuging.", "Balance tubes in opposite positions, as for any centrifuge load."])]),
    ("Not covered", ["Use in rotors or adapters not designed for 50 ml conical tubes is not covered by this note."]),
]
