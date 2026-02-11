import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_bmc(blocks, canvas_title, canvas_subtitle, scored_items=None):
    if scored_items is None:
        scored_items = {}

    fig, ax = plt.subplots(figsize=(20, 13))
    ax.set_xlim(0, 12.8)
    ax.set_ylim(0, 12.2)

    # Theme Colors (Backgrounds)
    colors = {
        "supply": {"bg": "#EBF8FF", "border": "#2B6CB0", "text": "#1A365D"},
        "value": {"bg": "#FFF5F5", "border": "#E53E3E", "text": "#742A2A"},
        "market": {"bg": "#E6FFFA", "border": "#319795", "text": "#234E52"},
        "money": {"bg": "#F0FFF4", "border": "#38A169", "text": "#22543D"}
    }

    # --- SCORING COLOR MAP ---
    # 1: Red (Weak/Risk)
    # 2: Amber/Orange (Normal/Average) - Darker yellow for readability
    # 3: Green (Strong/Advantage)
    score_colors = {
        1: "#D32F2F",  # Red
        2: "#E65100",  # Dark Amber/Orange (Yellow is too hard to read)
        3: "#2E7D32"  # Strong Green
    }

    for x, y, w, h, title, content, theme in blocks:
        # Draw Box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                      facecolor=colors[theme]["bg"],
                                      edgecolor=colors[theme]["border"], linewidth=2.5)
        ax.add_patch(rect)

        # Draw Title
        ax.text(x + 0.15, y + h - 0.4, title, weight='bold', fontsize=13,
                color=colors[theme]["border"], ha='left')

        # --- RENDER TEXT LINE BY LINE ---
        lines = content.split('\n')
        current_y = y + h - 0.9
        line_spacing = 0.28

        for line in lines:
            # Default Style
            text_color = colors[theme]["text"]
            font_weight = 'normal'

            # Check for Scoring Matches
            # We look if any keyword in our dictionary exists in the current line
            for keyword, score in scored_items.items():
                if keyword in line:
                    text_color = score_colors.get(score, text_color)
                    font_weight = 'bold'  # Make scored items bold to stand out
                    break

            ax.text(x + 0.15, current_y, line, fontsize=12, verticalalignment='top',
                    color=text_color, weight=font_weight)

            current_y -= line_spacing

    plt.axis('off')

    # Title & Subtitle
    fig.text(0.5, 0.93, canvas_title, ha='center', fontsize=24, weight='bold', color='#1A365D')
    #fig.text(0.5, 0.90, canvas_subtitle, ha='center', fontsize=14, color='#4A5568')

    # --- LEGEND ---
    # Draw a small legend at the bottom to explain the colors
    legend_y = 0
    fig.text(0.35, legend_y, "■ Weak / Risk (Score 1)", color=score_colors[1], weight='bold', fontsize=10, ha='center')
    fig.text(0.50, legend_y, "■ Normal / Developing (Score 2)", color=score_colors[2], weight='bold', fontsize=10,
             ha='center')
    fig.text(0.65, legend_y, "■ Strong / Competitive (Score 3)", color=score_colors[3], weight='bold', fontsize=10,
             ha='center')

    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)

    filename = f"{canvas_title}.png"
    plt.savefig(filename, bbox_inches='tight', dpi=300)
    print(f"Canvas saved as {filename}")
    plt.show()


if __name__ == "__main__":
    # --- DEFINE YOUR SCORES HERE ---
    # Dictionary format: "Keyword substring": Score (1, 2, or 3)
    byd_item_scores = {
        # SCORE 3 (Green - STRONG): The Core Tech & Partners
        "Blade Battery": 3,
        "In-House Mfg": 3,
        "Cost Efficiency": 3,
        "Mass": 3,
        "EV": 3,

        # SCORE 2 (Amber - NORMAL/DEVELOPING): Brand & Localization
        "Brand": 2,  # Brand is growing but not yet dominant globally like Toyota
        "Engagement": 2,
        "Hungary":2,
        "NVIDIA":2,
        "Localization costs": 2,

        # SCORE 1 (Red - WEAK/RISK): Service & Logistics bottlenecks
        "Proximity Service": 1,  # The biggest customer complaint (Parts delays)
        "Global Logistics": 1,  # High shipping costs/risks (Ro-Ro fleet is new)
        "Yangwang": 1,  # High shipping costs/risks (Ro-Ro fleet is new)
    }

    BYD_blocks = [
        # --- BOTTOM ROW: FINANCE ---
        (0.2, 0.3, 6.0, 3.8, "Cost Structure",
         "• Legacy & Core:\n  - In-House Mfg (Low Variable Cost)\n  - Manufacturing Labor\n\n"
         "• Procurement:\n  - Tariff Mgmt (Lithium Control)\n\n"
         "• Growth Investments:\n  - High R&D\n  - Localization costs\n  - Compliance costs",
         "money"),

        (6.4, 0.3, 6.1, 3.8, "Revenue Streams",
         "• Automotive:\n  - Passenger EVs & PHEVs\n  - Commercial Buses/Trucks\n  - Auto Parts & Batteries\n\n"
         "• Electronics:\n  - Utility-Scale Energy Storage\n  - Smart Device Components\n\n"
         "• Other: Corporate/Misc",
         "money"),

    # --- LEFT COLUMN: SUPPLY ---
        (0.2, 4.1, 2.7, 7.4, "Key Partners",
         "• Tech Innovation:\n  - NVIDIA (Drive Thor AI)\n  - Hesai (Lidar)\n  - Toyota (BTET R&D)\n\n"
         "• Govt & Localization:\n  - Hungary, Turkey, Brazil Factories\n  - Sigma Lithium (Brazil Mining)\n\n"
         "• Brand & Market Presence:\n  - UEFA Euro\n  - FC Inter Milan",
         "supply"),

        # --- MIDDLE-LEFT COLUMN: ACTIVITIES ---
        (3.1, 7.6, 2.6, 3.9, "Key Activities",
         "• Tech Leadership:\n  - 'XUANJI' Smart Architecture\n  - Blade Battery & Solid-State\n\n"
         "• Vertical Integration:\n  - Resource Sovereignty (Mines)\n  - SiC Chip Production\n\n"
         "• Global Ops:\n  - 'Ro-Ro' Shipping Fleet",
         "supply"),

        (3.1, 4.1, 2.6, 3.6, "Key Resources",
         "• Core Tech:\n  - Battery e-Platform 3.0 & DM-i 5.0\n\n"
         "• Infrastructure:\n  - 70-75% In-House Mfg\n  - 'Glocal' Production Hubs\n\n"
         "• Intellectual Capital:\n  - IP & 90k+ R&D Engineers",
         "supply"),

        # --- CENTER COLUMN: VALUE PROPOSITIONS ---
        (5.9, 4.1, 3.0, 7.4, "Value Propositions",
         "• Trust & Performance:\n  - 'Blade' Battery Standard\n  - Lifetime Warranty Quality\n\n"
         "• Choice & Logic:\n  - Multi-Path (EV + Hybrid)\n  - Tech-Democratization\n\n"
         "• Global Scale:\n  - Full-Stack Cost Efficiency\n  - Glocalized Delivery\n\n"
         "• Social Impact:\n  - Zero-Emission '7+4' Architect\n  - Energy Ecosystem (PV + Storage + EV)",
         "value"),

        # --- RIGHT COLUMN: MARKET ---
        (9.1, 7.6, 3.4, 3.9, "Customer Relationships",
         "• Lifecycle Management:\n  - TCO-Focused Care\n  - 'Glocal' Proximity Service\n\n"
         "• Engagement:\n  - Co-Creation Feedback Loops\n\n"
         "• Community:\n  - Value Partnering & Eco-Mission Advocacy",
         "market"),

        (9.1, 4.1, 3.4, 3.6, "Channels & Segments",
         "Target Segments:\n"
         "• Mass: Dynasty & Ocean Series\n"
         "• Premium: Yangwang, Denza, FCB\n"
         "• B2B/Govt: Buses, Taxis, Fleets\n"
         "• Industrial: Batteries (Tesla, Xiaomi)\n\n"
         "Key Channels:\n"
         "• Hybrid Retail: 4S Dealers + App\n"
         "• Global: DTC Showrooms (Premium)",
         "market")
    ]

    NISSAN_blocks = [
        # --- BOTTOM ROW: FINANCE ---
        (0.2, 0.3, 6.0, 3.8, "Cost Structure",
         "• Legacy & Core:\n  - Capital Asset \n  - Manufacturing Labor\n\n"
         "• Procurement:\n  - Tariff \n  - Supply Chain & Materials \n\n"
         "• Growth Investments:\n  - High R&D (Modular Development)\n",
         "money"),

        (6.4, 0.3, 6.1, 3.8, "Revenue Streams",
         "• Core Automotive:\n  - ICE/Hybrid:Rogue, Sentra, and Frontier\n\n"
         "• Electrification: Ariya, LEAF\n\n"
         "• Financial Services: Nissan Motor Acceptance Company (NMAC)\n\n"
         "• Service:\n  - Software & Licensing, \n  - Afters-ales & Parts",
         "money"),

        # --- LEFT COLUMN: SUPPLY ---
        (0.2, 4.1, 2.7, 7.4, "Key Partners",
         "• Global Operations:\n  - Renault–Nissan–Mitsubishi Alliance\n  - Mitsubishi Motors \n - Tesla (NACS)\n\n"
         "• Customer & Brand Extension:\n  - CAFU & YallaCompare(Customer Exp)\n  - Anaplan(Digital TF)\n\n"
         "• Geographic Expansion:\n  - Dongfeng Motor Group\n  - Tan Chong Motor Holdings\n\n"
         "• Supply Chain:\n  - Envision AESC (NCM/LMO)\n  - SK On (NCM)\n\n"
         "• Tech Innovation:\n  - Software-Defined Vehicles (Honda )\n  - Dry electrode manufacturing (LiCAP)",
         "supply"),

        # --- MIDDLE-LEFT COLUMN: ACTIVITIES ---
        (3.1, 7.6, 2.6, 3.9, "Key Activities",
         "• Market Optimization:\n  - 'The Arc Plan'-balancing EVs&ICE\n  - The Re:Nissan Recovery Plan\n\n"
         "• Strategic Alliance:\n  - Alliance-Scale Platform Sharing\n  - Feasibility-Led Intelligence Co-op\n\n"
         "• Tech Innovation: 'All-Solid-State Batteries",
         "supply"),

        (3.1, 4.1, 2.6, 3.6, "Key Resources",
         "• Core Tech:\n  - ASSB Prototype & e-POWER\n\n"
         "• Relational:\n  - CMF Architecture\n  - Global Alliances Ecosystem\n\n"
         "• Intellectual Capital:\n  - IP & Monetized Assets & R&D Talents",
         "supply"),

        # --- CENTER COLUMN: VALUE PROPOSITIONS ---
        (5.9, 4.1, 3.0, 7.4, "Value Propositions",
         "• Trust & Safety:\n  - Customer-Centric Exp\n  - Solid-State Performance\n  - Intelligent Co-Pilot Safety\n\n"
         "• Dependability & Choice:\n  - Multi-Path (ICE,e-Power,EV)\n  - Tech-Democratization\n\n"
         "• Global Scale:\n  - Modular Manufacturing\n  - Global Logistics\n\n"
         "• Social Impact:\n  - Carbon Neutrality & Zero-emission",
         "value"),

        # --- RIGHT COLUMN: MARKET ---
        (9.1, 7.6, 3.4, 3.9, "Customer Relationships",
         "• Personal Assistance:\n  - NissanConnect (Specialist)\n  - MyNISSAN App\n\n"
         "• Engagement:\n  - Co-Creation Feedback Loops\n\n"
         "• Community:\n  - NISSAN ENERGY charging networks\n  - EV sustainability initiatives",
         "market"),

        (9.1, 4.1, 3.4, 3.6, "Channels & Segments",
         "Target Segments:\n"
         "• Value-Driven: Versa, Sentra\n"
         "• Mainstream Family: Rogue, Pathfinder\n"
         "• EV & Eco-Conscious: Ariya, LEAF\n"
         "• B2B: Light Commercial Vehicle\n\n"
         "Key Channels:\n"
         "• Dealer Network: 3500+ locations globally\n"
         "• Digital Platforms: Nissan@Home + NISSAN ONE",
         "market")
    ]

    nissan_item_scores = {
        # SCORE 3 (Green - STRONG): The Core Tech & Partners
        "Alliance": 3,
        "Personal": 3,
        "Brand": 3,
        "Dependability":3,
        "Engagement": 3,

        # SCORE 2 (Amber - NORMAL/DEVELOPING): Brand & Localization
        "Tariff": 2,
        "Material": 2,
        "Capital Asset": 2,

        # SCORE 1 (Red - WEAK/RISK): Service & Logistics bottlenecks
        "Electrification:":1,
        "Proximity Service": 1,  # The biggest customer complaint (Parts delays)
        "EV &": 1,  # High shipping costs/risks (Ro-Ro fleet is new)
    }

    byd_title = "BYD BUSINESS MODEL CANVAS"
    byd_sub_title = "Strategies: Vertical Integration & Brand Improvement & Global Expansion via localized manufacturing"

    nissan_title = "NISSAN BUSINESS MODEL CANVAS"
    nissan_sub_title = "Strategies: Electrification Leadership & Product and Brand Revitalization & Global market optimization"

    draw_bmc(BYD_blocks, byd_title, byd_sub_title, byd_item_scores)
    draw_bmc(NISSAN_blocks, nissan_title, nissan_sub_title, nissan_item_scores)