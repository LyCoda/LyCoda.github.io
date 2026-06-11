window.PORTFOLIO_PROJECTS = [
  {
    id: "01",
    slug: "fnirs-classification",
    title:
      "fNIRS Classification for Neurodivergent and Neurotypical Participants During Complex Walking Tasks",
    shortTitle: "fNIRS Classification for Complex Walking Tasks",
    navLabel: "fNIRS ML",
    status: "In progress",
    description:
      "A research machine-learning case study translating modelled fNIRS haemodynamic responses into leakage-safe participant-level classification features.",
    role: "MSc Dissertation Researcher",
    focus: "Biomedical ML, fNIRS features, validation discipline",
    tools: "Python, scikit-learn, SPM.mat files, GLM beta estimates, cross-validation",
    outcome:
      "Built a defensible SPM beta-based classification workflow for small-sample biomedical data. Currently in progress.",
    image: "images/projects/fnirs.png",
    imageAlt:
      "Complex walking-task diagram used to frame an fNIRS classification project.",
    intro:
      "The project shifted from raw signal preprocessing toward a defensible ML pipeline built from SPM-generated haemodynamic response outputs.",
    caseStudy: {
      snapshot: [
        {
          label: "Problem",
          value:
            "Can fNIRS-derived brain activation features distinguish neurodivergent and neurotypical participants during complex walking tasks?",
        },
        {
          label: "Approach",
          value:
            "Validate participant SPM files, extract GLM beta features, construct compact feature sets, and compare classifiers under leakage-safe evaluation.",
        },
        {
          label: "My Role",
          value:
            "Owned the end-to-end ML workflow, from SPM output validation to feature generation, model comparison, and performance interpretation.",
        },
        {
          label: "Key Challenge",
          value:
            "Small samples, high-dimensional features, unstable fold performance, and high risk of participant-level leakage.",
        },
        {
          label: "Outcome",
          value:
            "A working, academically grounded pipeline focused on transparent evaluation rather than inflated accuracy.",
        },
      ],
      context: [
        "Functional near-infrared spectroscopy measures changes in oxygenated and deoxygenated haemoglobin in cortical tissue. In this project, fNIRS is used to study prefrontal activity during walking tasks under more complex environmental conditions.",
        "The final working data is based on participant-level SPM.mat outputs containing GLM design information, beta estimates, and task regressors. That made the project less about raw preprocessing and more about converting modelled haemodynamic responses into interpretable ML features.",
      ],
      built: [
        {
          label: "SPM validation",
          value:
            "Checked participant-level SPM outputs before feature generation and excluded unusable files with missing or invalid design information.",
        },
        {
          label: "Feature tables",
          value:
            "Generated task, contrast, condition, and ROI-level feature sets from beta estimates for controlled comparison.",
        },
        {
          label: "ML evaluation",
          value:
            "Built classification workflows with scaling, feature selection, and model evaluation kept inside the correct training folds.",
        },
        {
          label: "Performance reporting",
          value:
            "Used balanced accuracy, confusion matrices, and participant-level stability checks to interpret performance honestly.",
        },
      ],
      workflowTitle: "Pipeline Overview",
      workflow: [
        "SPM.mat files",
        "Beta extraction",
        "ROI / task / contrast features",
        "Leakage-safe CV",
        "Balanced evaluation",
      ],
      tableTitle: "Feature Engineering Direction",
      table: [
        {
          label: "ROI summaries",
          value: "Reduce dimensionality and make haemodynamic patterns easier to interpret.",
        },
        {
          label: "Task-context features",
          value: "Capture differences across walking and auditory task contexts.",
        },
        {
          label: "Contrast features",
          value: "Focus on meaningful condition differences instead of raw task values alone.",
        },
        {
          label: "Lighting-condition summaries",
          value: "Test whether blue/yellow environmental conditions carry useful signal.",
        },
        {
          label: "Participant stability",
          value: "Check whether predictions are consistent or heavily fold-dependent.",
        },
      ],
      decisions: [
        {
          label: "Leakage-safe validation",
          value:
            "Scaling, feature selection, tuning, and evaluation stay inside the correct folds so test information is not leaked into training.",
        },
        {
          label: "Compact feature design",
          value:
            "ROI-level and contrast-based features limit uncontrolled feature expansion in a small biomedical dataset.",
        },
        {
          label: "Balanced metrics",
          value:
            "Balanced accuracy and participant-level behaviour matter more than a single headline accuracy score.",
        },
        {
          label: "Academic defensibility",
          value:
            "The project prioritises a transparent workflow that can be discussed and improved with supervisors.",
        },
      ],
      outcomes: [
        {
          label: "Built",
          value: "A working SPM beta-based fNIRS classification pipeline.",
        },
        {
          label: "Developed",
          value: "Multiple handcrafted feature tables for controlled model comparison.",
        },
        {
          label: "Identified",
          value:
            "Small-sample instability as a central limitation shaping future feature and evaluation choices.",
        },
        {
          label: "Currently",
          value:
            "Refining feature comparisons, evaluation reporting, and dissertation-ready interpretation.",
        },
      ],
      demonstrates: [
        "Biomedical machine learning",
        "Feature engineering",
        "Validation discipline",
        "Research communication",
      ],
      reflection: [
        "A careful biomedical ML pipeline is only as strong as its validation design.",
        "The next stage is to refine features without turning the model into a high-dimensional noise detector.",
      ],
    },
  },
  {
    id: "02",
    slug: "bone-healing-monitoring-device",
    title: "OsteoTrack / Bone Healing Monitoring Device",
    shortTitle: "OsteoTrack Bone Healing Monitoring Device",
    navLabel: "OsteoTrack",
    status: "Concept project",
    description:
      "A medtech innovation proposal for non-invasive fracture healing monitoring, built around vibration sensing, accelerometers, and clinician-facing AI support.",
    role: "Device Concept Developer / Communications Officer / Marketing Officer",
    focus: "Clinical need, NHS adoption, market strategy, medical-device translation",
    tools:
      "Vibration sensing concept, accelerometers, AI-assisted trend analysis, NHS pathway analysis, pricing strategy",
    outcome:
      "Developed a realistic orthopaedic monitoring proposal for fracture follow-up support without claiming clinical deployment.",
    image: "images/projects/bone-healing.png",
    imageAlt:
      "Wearable bone healing monitoring concept shown on an upper arm.",
    intro:
      "OsteoTrack translates a fracture non-union monitoring problem into a device, governance, and adoption proposal shaped around realistic NHS use.",
    caseStudy: {
      snapshot: [
        {
          label: "Problem",
          value:
            "Fracture non-union can be difficult to identify early, while follow-up often depends on repeated appointments and X-ray imaging.",
        },
        {
          label: "Approach",
          value:
            "Propose a non-invasive cuff-based device using vibration response and accelerometer data to track healing trends over time.",
        },
        {
          label: "My Role",
          value:
            "Developed market research, pricing model, marketing strategy, fundraising plan, executive summary, and NHS positioning.",
        },
        {
          label: "Key Challenge",
          value:
            "Balance technical plausibility with regulation, AI governance, procurement, safety, adoption, and clinical responsibility.",
        },
        {
          label: "Outcome",
          value:
            "A clinically and commercially framed proposal for an AI-supported orthopaedic monitoring platform.",
        },
      ],
      context: [
        "OsteoTrack is a non-invasive medical device concept designed to monitor fracture healing progression and support earlier detection of possible fracture non-union.",
        "The concept supports clinicians rather than replacing clinical judgement. It was positioned as a realistic healthcare product proposal for NHS adoption, not as a validated clinical device.",
      ],
      built: [
        {
          label: "Market research",
          value:
            "Identified the clinical customer, NHS route to market, adoption pressures, and relevant competitor landscape.",
        },
        {
          label: "Pricing model",
          value:
            "Proposed per-patient pricing to reduce upfront adoption barriers and align revenue with clinical usage.",
        },
        {
          label: "Commercial positioning",
          value:
            "Linked the device to remote monitoring, virtual fracture clinics, workflow efficiency, and AI-enabled healthcare strategy.",
        },
        {
          label: "Executive summary",
          value:
            "Helped communicate the product proposal across clinical need, technical feasibility, regulation, and funding.",
        },
      ],
      workflowTitle: "Clinical Need to NHS Adoption",
      workflow: [
        "Clinical need",
        "Device concept",
        "AI trend support",
        "Regulatory strategy",
        "NHS adoption model",
      ],
      tableTitle: "Device Logic",
      table: [
        {
          label: "Controlled vibration",
          value: "Applies a repeatable stimulus to the limb through a cuff-based device concept.",
        },
        {
          label: "Accelerometer response",
          value: "Measures vibrational response linked to changes in stiffness and resonance behaviour.",
        },
        {
          label: "Trend analysis",
          value: "Uses repeated measurements to track whether healing appears to follow a normal trajectory.",
        },
        {
          label: "Clinician review flag",
          value: "Positions AI as decision support that flags possible review needs, not as diagnosis.",
        },
      ],
      decisions: [
        {
          label: "AI as support",
          value:
            "The AI component was framed as trend-based decision support rather than an autonomous diagnostic system.",
        },
        {
          label: "NHS-first adoption",
          value:
            "The proposal focused on clinical workflow fit, procurement realism, and reducing fracture-service pressure.",
        },
        {
          label: "Per-patient pricing",
          value:
            "A usage-aligned model lowered the barrier compared with high upfront device purchasing.",
        },
        {
          label: "Regulatory readiness",
          value:
            "The concept considered MHRA classification, AI governance, data protection, safety, and clinical validation needs.",
        },
      ],
      outcomes: [
        {
          label: "Developed",
          value:
            "A non-invasive orthopaedic monitoring concept for fracture follow-up support.",
        },
        {
          label: "Positioned",
          value:
            "The product as a clinician-facing platform rather than a consumer wearable.",
        },
        {
          label: "Contributed",
          value:
            "Market, pricing, communications, fundraising, and executive-summary work.",
        },
        {
          label: "Explored",
          value:
            "How engineering, regulation, finance, procurement, and clinical workflow shape healthcare innovation.",
        },
      ],
      demonstrates: [
        "Medtech translation",
        "Commercial strategy",
        "AI governance",
        "Healthcare adoption",
      ],
      reflection: [
        "A promising device concept still needs a credible pathway through clinical value, regulation, procurement, and adoption.",
        "The strongest proposal treated AI as a bounded support tool, not as a replacement for clinicians.",
      ],
    },
  },
  {
    id: "03",
    slug: "redcap-feedback-workflow",
    title: "REDCap Orthopaedic Outcome Tracking System",
    shortTitle: "REDCap Orthopaedic Outcome Tracking",
    navLabel: "REDCap",
    status: "Work experience",
    description:
      "A digital health workflow for automating post-operative orthopaedic feedback collection from patients and surgeons through REDCap.",
    role: "Workflow Automation Developer",
    focus: "Clinical data capture, post-market feedback, survey automation, R&D training",
    tools:
      "REDCap, OrthopaedicScore.com scoring systems, automated email logic, outcome questionnaires",
    outcome:
      "Streamlined feedback collection by creating a repeatable workflow for structured orthopaedic outcome tracking.",
    image: "images/projects/redcap.png",
    imageAlt:
      "REDCap logo representing an orthopaedic outcome tracking workflow.",
    intro:
      "This project turned manual post-operative feedback collection into a structured REDCap workflow for orthopaedic implant outcome tracking.",
    caseStudy: {
      snapshot: [
        {
          label: "Problem",
          value:
            "Post-operative implant feedback was harder to track consistently when coordination depended on manual follow-up.",
        },
        {
          label: "Approach",
          value:
            "Implement validated orthopaedic scoring systems inside REDCap and automate survey distribution for patients and surgeons.",
        },
        {
          label: "My Role",
          value:
            "Built questionnaires, configured automated email workflows, organised forms by anatomy and context, and trained the R&D team.",
        },
        {
          label: "Key Challenge",
          value:
            "Translate established orthopaedic assessment scores into a usable digital workflow without introducing confidential data.",
        },
        {
          label: "Outcome",
          value:
            "A repeatable clinical feedback process for recovery, comfort, quality-of-life, and implant-performance insight.",
        },
      ],
      context: [
        "The workflow supported post-operative feedback collection for orthopaedic implant patients and surgeons. The scoring systems were based on validated questionnaires from OrthopaedicScore.com.",
        "The system supported KOLN 3D, a company involved in manufacturing metallic surgical implants, by making structured clinical feedback easier to collect and review.",
      ],
      built: [
        {
          label: "Questionnaire implementation",
          value:
            "Manually recreated relevant orthopaedic scoring systems inside REDCap with clear question and response structures.",
        },
        {
          label: "Email automation",
          value:
            "Configured automated survey distribution to reduce manual coordination and missed follow-ups.",
        },
        {
          label: "Anatomy-specific organisation",
          value:
            "Structured forms around anatomical region, surgical context, patient feedback, and surgeon input.",
        },
        {
          label: "Team training",
          value:
            "Trained the R&D team to manage surveys, monitor responses, and understand the data collection workflow.",
        },
      ],
      workflowTitle: "Feedback Loop",
      workflow: [
        "Patient / surgeon",
        "REDCap survey",
        "Automated tracking",
        "R&D review",
        "Implant feedback insight",
      ],
      tableTitle: "Workflow Before / After",
      table: [
        {
          label: "Before",
          value:
            "Manual coordination, inconsistent tracking, harder follow-up, and less centralised feedback review.",
        },
        {
          label: "After",
          value:
            "Automated survey distribution, structured responses, centralised tracking, and clearer R&D review.",
        },
      ],
      decisions: [
        {
          label: "Validated scoring systems",
          value:
            "Using established orthopaedic scores helped keep feedback clinically structured rather than informal.",
        },
        {
          label: "Automated email logic",
          value:
            "Automation made the workflow more repeatable and reduced reliance on ad hoc manual follow-up.",
        },
        {
          label: "Centralised tracking",
          value:
            "REDCap gave the team one place to monitor requests, responses, and follow-up status.",
        },
        {
          label: "Team handover",
          value:
            "Training the R&D team helped the system remain usable after initial implementation.",
        },
      ],
      outcomes: [
        {
          label: "Streamlined",
          value: "Post-operative feedback collection across patients and surgeons.",
        },
        {
          label: "Standardised",
          value: "Outcome scoring across different anatomical regions and surgical contexts.",
        },
        {
          label: "Improved",
          value: "Response tracking through centralised REDCap survey workflows.",
        },
        {
          label: "Supported",
          value:
            "Post-market feedback insight for implant comfort, quality of life, and surgeon review.",
        },
      ],
      demonstrates: [
        "Digital health workflows",
        "Clinical data capture",
        "Process automation",
        "Research operations",
      ],
      reflection: [
        "Small workflow decisions can make clinical feedback easier to collect, monitor, and reuse.",
        "This project showed how digital health infrastructure can support medical-device development beyond the device itself.",
      ],
    },
  },
  {
    id: "04",
    slug: "emg-controlled-robotic-arm",
    title: "Adaptive EMG Signal Control for a Robotic Arm",
    shortTitle: "Adaptive EMG Robotic Arm",
    navLabel: "EMG Arm",
    status: "Academic project",
    description:
      "A low-cost biomedical robotics proof-of-concept translating surface EMG muscle activity into Arduino-based servo control.",
    role: "BEng Dissertation Researcher",
    focus: "Biosignal control, assistive robotics, CAD design, embedded systems",
    tools: "Surface EMG, Arduino, servo motors, filtering, CAD, 3D-printable design",
    outcome:
      "Developed a structured low-cost EMG-to-motion robotic arm concept and control workflow.",
    image: "images/projects/emg-arm.jpg",
    imageAlt: "CAD render of a low-cost robotic prosthetic arm concept.",
    intro:
      "This project explored how physiological muscle signals can become control inputs for assistive robotic movement within a limited student-project budget and timeline.",
    caseStudy: {
      snapshot: [
        {
          label: "Problem",
          value:
            "Can surface EMG signals be processed and mapped into meaningful robotic arm movement using low-cost components?",
        },
        {
          label: "Approach",
          value:
            "Connect EMG sensing, filtering, control decisions, Arduino communication, and servo actuation into one proof-of-concept workflow.",
        },
        {
          label: "My Role",
          value:
            "Developed the concept, architecture, control strategy, mechanical direction, and signal-to-motion mapping.",
        },
        {
          label: "Key Challenge",
          value:
            "Build across programming, CAD, electronics, signal processing, and biosignal control under a short timeline and limited budget.",
        },
        {
          label: "Outcome",
          value:
            "A structured proof-of-concept showing how muscle activity can control robotic movement, without claiming clinical readiness.",
        },
      ],
      context: [
        "A myoelectric robotic arm is controlled using electrical activity generated by muscles. Surface electrodes detect EMG signals, which can then be processed and mapped to movement commands.",
        "The project was not intended to create a clinically ready prosthetic arm. Its goal was to demonstrate a biomedical robotics principle: physiological signals can be translated into external mechanical motion.",
      ],
      built: [
        {
          label: "System architecture",
          value:
            "Mapped EMG electrodes, signal processing, Arduino control, and servo actuation into one coherent control pathway.",
        },
        {
          label: "Control strategy",
          value:
            "Explored how muscle activity from different regions could correspond to elbow, wrist, and grip functions.",
        },
        {
          label: "Mechanical direction",
          value:
            "Worked on a low-cost robotic arm design with servo-driven joints and simplified modular components.",
        },
        {
          label: "Integration thinking",
          value:
            "Balanced noisy biological signals, limited inputs, real-time response, cost, and achievable mechanical complexity.",
        },
      ],
      workflowTitle: "Signal-to-Motion Pipeline",
      workflow: [
        "Muscle contraction",
        "Surface EMG",
        "Filtering / processing",
        "Control decision",
        "Arduino",
        "Servo movement",
      ],
      tableTitle: "System Components",
      table: [
        {
          label: "EMG sensing",
          value: "Detects muscle activity through surface electrodes.",
        },
        {
          label: "Signal processing",
          value: "Filters and interprets signals before movement mapping.",
        },
        {
          label: "Arduino control",
          value: "Converts interpreted signal states into motor commands.",
        },
        {
          label: "Servo motors",
          value: "Drive robotic movement for grasping and joint actuation.",
        },
        {
          label: "CAD structure",
          value: "Supports low-cost mechanical prototyping and modular design.",
        },
      ],
      decisions: [
        {
          label: "Low-cost simplification",
          value:
            "Reduced mechanical complexity and servo count to keep the concept closer to the budget and timeline.",
        },
        {
          label: "Modular wrist direction",
          value:
            "Simplifying the wrist helped keep cost and integration demands lower.",
        },
        {
          label: "Proof-of-concept scope",
          value:
            "The project focused on demonstrating signal-to-motion feasibility rather than clinical readiness.",
        },
        {
          label: "Physiology-led control",
          value:
            "The design used muscle activity as the control source instead of joystick or button input.",
        },
      ],
      outcomes: [
        {
          label: "Designed",
          value: "A low-cost EMG-controlled robotic arm architecture.",
        },
        {
          label: "Explored",
          value: "How muscle signals can be converted into Arduino-based actuation.",
        },
        {
          label: "Developed",
          value:
            "A structured control workflow connecting sensing, processing, and servo movement.",
        },
        {
          label: "Learned",
          value:
            "Practical constraints around noisy signals, limited inputs, latency, repeatability, and mechanical trade-offs.",
        },
      ],
      demonstrates: [
        "Biomedical robotics",
        "Human-machine interfaces",
        "Embedded prototyping",
        "Assistive technology design",
      ],
      reflection: [
        "The project made the difficulty of real-time biological control very concrete.",
        "It also showed the value of simplifying scope when building interdisciplinary prototypes under hard constraints.",
      ],
    },
  },
];
