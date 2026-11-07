// CyberShield Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    startLiveUpdates();
    initializeCharts();
});

// Dashboard Initialization
function initializeDashboard() {
    console.log('CyberShield Dashboard Initialized');
    updateThreatsCount();
    populateThreatFeed();
}

// Live Data Updates
function startLiveUpdates() {
    // Simulate live data updates every 5 seconds
    setInterval(() => {
        updateThreatsCount();
        addNewThreat();
        updateCharts();
    }, 5000);
}

// Threat Management
function updateThreatsCount() {
    const threatsCount = Math.floor(Math.random() * 100) + 50;
    document.getElementById('threats-count').textContent = threatsCount;
}

function populateThreatFeed() {
    const threatList = document.getElementById('threat-list');
    threatList.innerHTML = '';
    
    const sampleThreats = [
        {
            type: 'Malware Detection',
            details: 'Suspicious executable detected from external IP',
            severity: 'critical',
            time: '2 minutes ago'
        },
        {
            type: 'Brute Force Attempt',
            details: 'Multiple failed login attempts on admin account',
            severity: 'high',
            time: '5 minutes ago'
        },
        {
            type: 'Phishing Attempt',
            details: 'Suspicious email with malicious attachment',
            severity: 'medium',
            time: '10 minutes ago'
        },
        {
            type: 'Port Scan',
            details: 'Multiple port connection attempts detected',
            severity: 'low',
            time: '15 minutes ago'
        }
    ];
    
    sampleThreats.forEach(threat => {
        threatList.appendChild(createThreatElement(threat));
    });
}

function addNewThreat() {
    const threatTypes = [
        'Malware', 'Phishing', 'Brute Force', 'DDoS', 'SQL Injection',
        'XSS Attack', 'Ransomware', 'Data Exfiltration'
    ];
    
    const severities = ['critical', 'high', 'medium', 'low'];
    const times = ['just now', '1 minute ago', '2 minutes ago'];
    
    const newThreat = {
        type: threatTypes[Math.floor(Math.random() * threatTypes.length)],
        details: `New ${threatTypes[Math.floor(Math.random() * threatTypes.length)].toLowerCase()} detected`,
        severity: severities[Math.floor(Math.random() * severities.length)],
        time: times[Math.floor(Math.random() * times.length)]
    };
    
    const threatList = document.getElementById('threat-list');
    if (threatList.children.length > 10) {
        threatList.removeChild(threatList.lastChild);
    }
    threatList.insertBefore(create极速飞艇开奖结果记录ThreatElement(newThreat), threatList.firstChild);
}

function createThreatElement(threat) {
    const div = document.createElement('div');
    div.className = 'threat-item';
    div.innerHTML = `
        <div class="threat-severity ${threat.severity}"></div>
        <div class="threat-content">
            <div class="threat-type">${threat.type}</div>
            <div class="threat-details">${threat.details}</div>
        </div>
        <div class="threat-time">${threat.time}</div>
    `;
    
    // Add click effect
    div.addEventListener('click', function() {
        this.style.transform = 'scale(0.98)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
    
    return div;
}

function refreshThreats() {
    const refreshBtn = document.querySelector('.refresh-btn');
    refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
    
    setTimeout(() => {
        populateThreatFeed();
        refreshBtn.innerHTML = '<i class="fas fa-sync"></i> Refresh';
        
        // Add refresh animation
        refreshBtn.classList.add('refreshing');
        setTimeout(() => {
            refreshBtn.classList.remove('refreshing');
        }, 1000);
    }, 1000);
}

// Chart Initialization
let threatTypeChart, trafficChart;

function initializeCharts() {
    // Threat Type Distribution Chart
    const threatTypeCtx = document.getElementById('threatTypeChart').getContext('2d');
    threatTypeChart = new Chart(threatTypeCtx, {
        type: 'doughnut',
        data: {
            labels: ['Malware', 'Phishing', 'Brute Force', 'DDoS', 'Other'],
            datasets: [{
                data: [35, 25, 20, 15, 5],
                backgroundColor: [
                    '#ff4444',
                    '#ff6b35',
                    '#ffc107',
                    '#00d4ff',
                    '#888888'
                ],
                borderWidth: 0,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    // Network Traffic Chart
    const trafficCtx = document.getElementById('trafficChart').getContext('2d');
    trafficChart = new Chart(trafficCtx, {
        type: 'line',
        data: {
            labels: ['00:00', '04:00', '08:00', '12:00', '16:极速飞艇开奖结果记录00', '20:00'],
            datasets: [{
                label: 'Incoming Traffic',
                data: [120, 150, 300, 450, 200, 180],
                borderColor: '#00d4ff',
                backgroundColor: 'rgba(0, 212, 255, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#00d4ff',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }, {
                label: 'Outgoing Traffic',
                data: [80, 120, 250, 380, 150, 120],
                borderColor: '#ff6b35',
                backgroundColor: 'rgba(255, 107, 53, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#ff6b35',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        font: {
                            size: 12
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#cccccc'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#cccccc'
                    }
                }
            }
        }
    });
}

function updateCharts() {
    // Update threat type chart with random data
    if (threatTypeChart) {
        threatTypeChart.data.datasets[0].data = [
            Math.floor(Math.random() * 50) + 20,
            Math.floor(Math.random() * 40) + 15,
            Math.floor(Math.random() * 30) + 10,
            Math.floor(Math.random() * 20) + 5,
            Math.floor(Math.random() * 10) + 2
        ];
        threatTypeChart.update();
    }

    // Update traffic chart with new data points
    if (trafficChart) {
        const newIncoming = Math.floor(Math.random() * 500) + 100;
        const newOutgoing = Math.floor(Math.random() * 400) + 80;
        
        // Shift data and add new point
        trafficChart.data.datasets[0].data.push(newIncoming);
        trafficChart.data.datasets[0].data.shift();
        
        trafficChart.data.datasets[1].data.push(newOutgoing);
        trafficChart.data.datasets[1].data.shift();
        
        trafficChart.update();
    }
}

// System Health Animation
function animateHealthBars() {
    const healthBars = document.querySelectorAll('.health-progress');
    healthBars.forEach(bar => {
        const randomWidth = Math.floor(Math.random() * 30) + 20;
        bar.style.width = randomWidth + '%';
        bar.previousElementSibling.textContent = randomWidth + '%';
    });
}

// Start health bar animations
setInterval(animateHealthBars, 3000);

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'r':
                e.preventDefault();
                refreshThreats();
                break;
            case '1':
                e.preventDefault();
                document.querySelector('[href="#dashboard"]').click();
                break;
            case '2':
                e.preventDefault();
                document.querySelector('[href="#threats"]').click();
                break;
        }
    }
});

// Smooth Scrolling for Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Threat Detection Dataset
const threatDataset = {
    patterns: [
        {
            name: "SQL Injection",
            type: "Web Attack",
            patterns: ["SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "UNION", "OR 1=1"],
            severity: "critical",
            confidence: 95,
            description: "Malicious SQL queries attempting to manipulate database"
        },
        {
            name: "XSS Attack",
            type: "Web Attack", 
            patterns: ["<script>", "javascript:", "onerror=", "onload=", "alert("],
            severity: "high",
            confidence: 88,
            description: "Cross-site scripting attempt detected in input data"
        },
        {
            name: "Port Scan",
            type: "Reconnaissance",
            patterns: ["multiple ports", "connection attempts", "port 22", "port 3389"],
            severity: "medium",
            confidence: 75,
            description: "Multiple port connection attempts indicating network reconnaissance"
        },
        {
            name: "DDoS Attempt",
            type: "Network Flood",
            patterns: ["high traffic", "multiple requests", "flood", "bandwidth"],
            severity: "critical",
            confidence: 92,
            description: "Distributed Denial of Service attack pattern detected"
        },
        {
            name: "Brute Force",
            type: "Authentication Attack",
            patterns: ["failed login", "multiple attempts", "password guess", "auth failure"],
            severity: "high",
            confidence: 85,
            description: "Multiple failed authentication attempts detected"
        }
    ],
    
    ipReputation: {
        "192.168.1.100": { reputation: "malicious", score: 95 },
        "10.0.0.50": { reputation: "suspicious", score: 70 },
        "172.16.0.1": { reputation: "clean", score: 10 }
    },
    
    portThreats: {
        "22": "SSH Brute Force",
        "23": "Telnet Attack",
        "80": "HTTP Attacks",
        "443": "HTTPS Attacks", 
        "3389": "RDP Attacks",
        "5900": "VNC Attacks"
    }
};

// Threat Detection Function
function analyzeThreat() {
    const sourceIp = document.getElementById('source-ip').value;
    const destIp = document.getElementById('destination-ip').value;
    const protocol = document.getElementById('protocol').value;
    const port = document.getElementById('port').value;
    const payloadSize = document.getElementById('payload-size').value;
    const requestType = document.getElementById('request-type').value;
    
    // Validate inputs
    if (!sourceIp || !destIp || !protocol) {
        alert('Please fill in all required fields (Source IP, Destination IP, Protocol)');
        return;
    }
    
    // Simulate analysis (in real system, this would call the backend API)
    const detectionResult = detectThreatPatterns({
        source_ip: sourceIp,
        destination_ip: destIp,
        protocol: protocol,
        port: parseInt(port),
        payload_size: parseInt(payloadSize),
        request_type: requestType
    });
    
    // Display results
    displayResults(detectionResult);
    
    // Add to threat feed
    addToThreatFeed(detectionResult);
}

function detectThreatPatterns(data) {
    let detectedThreats = [];
    let maxSeverity = "low";
    let maxConfidence = 0;
    
    // Check IP reputation
    if (threatDataset.ipReputation[data.source_ip]) {
        const ipInfo = threatDataset.ipReputation[data.source_ip];
        detectedThreats.push({
            name: "Malicious IP",
            type: "IP Reputation",
            severity: ipInfo.score > 80 ? "critical" : "high",
            confidence: ipInfo.score,
            description: `Source IP ${data.source_ip} has ${ipInfo.reputation} reputation`
        });
    }
    
    // Check port threats
    if (threatDataset.portThreats[data.port]) {
        detectedThreats.push({
            name: threatDataset.portThreats[data.port],
            type: "Port-based Threat",
            severity: "medium",
            confidence: 65,
            description: `Port ${data.port} is commonly targeted for attacks`
        });
    }
    
    // Check for large payloads (potential DDoS)
    if (data.payload_size > 10000) {
        detectedThreats.push({
            name: "Large Payload",
            type: "Network Anomaly",
            severity: "medium",
            confidence: 70,
            description: `Unusually large payload size: ${data.payload_size} bytes`
        });
    }
    
    // Find the highest severity threat
    if (detectedThreats.length > 0) {
        const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
        detectedThreats.forEach(threat => {
            if (severityOrder[threat.severity] > severityOrder[maxSeverity]) {
                maxSeverity = threat.severity;
                maxConfidence = threat.confidence;
            }
        });
    }
    
    return {
        threats: detectedThreats,
        primaryThreat: detectedThreats.length > 0 ? detectedThreats[0] : null,
        severity: maxSeverity,
        confidence: maxConfidence,
        timestamp: new Date().toISOString()
    };
}

function displayResults(result) {
    const resultsContainer = document.getElementById('results-container');
    const attackType = document.getElementById('attack-type');
    const attackName = document.getElementById('attack-name');
    const confidence = document.getElementById('confidence');
    const riskScore = document.getElementById('risk-score');
    const attackDetails = document.getElementById('attack-details');
    
    if (result.threats.length === 0) {
        attackType.textContent = "No threats detected";
        attackName.textContent = "Clean traffic";
        confidence.textContent = "100%";
        riskScore.textContent = "0";
        attackDetails.textContent = "No malicious patterns detected in the input data.";
    } else {
        const primary = result.primaryThreat;
        attackType.textContent = primary.type;
        attackType.setAttribute('data-severity', result.severity);
        attackName.textContent = primary.name;
        attackName.setAttribute('data-severity', result.severity);
        confidence.textContent = `${result.confidence}%`;
        confidence.setAttribute('data-severity', result.severity);
        
        // Calculate risk score based on severity and confidence
        const riskScores = { critical: 90, high: 70, medium: 50, low: 30 };
        const riskScoreValue = Math.min(100, riskScores[result.severity] + (result.confidence / 100 * 10));
        riskScore.textContent = Math.round(riskScoreValue);
        riskScore.setAttribute('data-severity', result.severity);
        
        // Build details text
        let detailsText = primary.description + "\n\n";
        if (result.threats.length > 1) {
            detailsText += `Additional threats detected (${result.threats.length - 1}):\n`;
            result.threats.slice(1).forEach((threat, index) => {
                detailsText += `${index + 1}. ${threat.name} (${threat.type})\n`;
            });
        }
        attackDetails.textContent = detailsText;
    }
    
    resultsContainer.style.display = 'block';
    
    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function addToThreatFeed(result) {
    if (result.threats.length === 0) return;
    
    const threatList = document.getElementById('threat-list');
    const threatItem = document.createElement('div');
    threatItem.className = 'threat-item';
    
    threatItem.innerHTML = `
        <div class="threat-severity ${result.severity}"></div>
        <div class="threat-content">
            <div class="threat-type">${result.primaryThreat.name}</div>
            <div class="threat-details">${result.primaryThreat.description}</div>
        </div>
        <div class="threat-time">just now</div>
    `;
    
    threatList.insertBefore(threatItem, threatList.firstChild);
    
    // Update threats count
    const currentCount = parseInt(document.getElementById('threats-count').textContent);
    document.getElementById('threats-count').textContent = currentCount + 1;
}

// Performance Monitoring
let performanceMetrics = {
    loadTime: performance.now(),
    threatUpdates: 0,
    chartUpdates: 0,
    detections: 0
};

setInterval(() => {
    performanceMetrics.threatUpdates++;
    performanceMetrics.chartUpdates++;
    
    // Log performance every minute
    if (performanceMetrics.threatUpdates % 12 === 0) {
        console.log('Performance Metrics:', {
            uptime: Math.floor((performance.now() - performanceMetrics.loadTime) / 1000) + 's',
            threatUpdates: performanceMetrics.threatUpdates,
            chartUpdates: performanceMetrics.chartUpdates,
            detections: performanceMetrics.detections,
            memory: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) + 'MB' : 'N/A'
        });
    }
}, 5000);
