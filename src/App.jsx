import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [activeSection, setActiveSection] = useState('hero')
  const [isVisible, setIsVisible] = useState(false)
  const [profilePhoto, setProfilePhoto] = useState(null)
  const [profilePhotoName, setProfilePhotoName] = useState('')

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const handlePhotoChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = () => setProfilePhoto(reader.result)
    reader.readAsDataURL(file)
    setProfilePhotoName(file.name)
  }

  const projects = [
    {
      title: 'Fintech Transaction App',
      description:
        'A comprehensive financial services platform that leverages digital technology to automate, speed up and simplify financial operations. Users can manage money, make payments, and invest directly from their smartphones or computers.',
      tech: ['Python', 'React', 'PostgreSQL'],
      icon: '💳',
    },
    {
      title: 'Zoom2YouTube Automation',
      description:
        'An intelligent automation tool that downloads Zoom recordings, allows users to select and customize video titles, and seamlessly pushes selected content to YouTube for easy sharing and distribution.',
      tech: ['Python', 'React'],
      icon: '🎥',
    },
    {
      title: 'Music Streamer App',
      description:
        'A desktop music streaming application designed to help users discover and play their preferred music with an intuitive interface for seamless playback.',
      tech: ['Python', 'React'],
      icon: '🎵',
    },
  ]

  const skills = [
    { name: 'Python', level: 90, icon: 'Py' },
    { name: 'React', level: 85, icon: '⚛' },
    { name: 'CSS', level: 80, icon: '' },
    { name: 'HTML', level: 85, icon: '🌐' },
    { name: 'PostgreSQL', level: 75, icon: 'DB' },
  ]

  const trustPoints = [
    {
      title: 'Reliable Development',
      detail: 'I follow standard software practices, deliver clean code, and commit to consistent milestones.',
      icon: '✓',
    },
    {
      title: 'Secure Architecture',
      detail: 'I build secure, scalable systems with strong data handling and real-world reliability.',
      icon: '🔒',
    },
    {
      title: 'User-First Experience',
      detail: 'I design interfaces that simplify workflows and make digital tools easy to adopt.',
      icon: '',
    },
  ]

  return (
    <div className={`app ${isVisible ? 'visible' : ''}`}>
      <nav className="navbar">
        <div className="nav-brand">
          <span className="brand-text">Justin</span>
          <span className="brand-subtitle">Software Developer</span>
        </div>
        <div className="nav-links">
          {['hero', 'about', 'projects', 'skills', 'contact'].map((section) => (
            <button
              key={section}
              className={`nav-link ${activeSection === section ? 'active' : ''}`}
              onClick={() => setActiveSection(section)}
            >
              {section.charAt(0).toUpperCase() + section.slice(1)}
            </button>
          ))}
        </div>
      </nav>

      <section className={`section hero-section ${activeSection === 'hero' ? 'active' : ''}`}>
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              Hi, I'm <span className="highlight">Justin</span>
            </h1>
            <h2 className="hero-subtitle">Full-Stack Software Developer</h2>
            <p className="hero-description">
              With 3 years of experience crafting digital solutions using Python, React, and PostgreSQL.
              I build scalable applications that automate, simplify, and improve everyday workflows.
            </p>
            <div className="hero-highlights">
              <div className="highlight-item">
                <span className="highlight-icon"></span>
                <span>Full-Stack Development</span>
              </div>
              <div className="highlight-item">
                <span className="highlight-icon"></span>
                <span>Performance Optimization</span>
              </div>
              <div className="highlight-item">
                <span className="highlight-icon"></span>
                <span>API Integration</span>
              </div>
              <div className="highlight-item">
                <span className="highlight-icon"></span>
                <span>User-Centric Design</span>
              </div>
            </div>
            <div className="hero-buttons">
              <button className="btn primary" onClick={() => setActiveSection('projects')}>
                View My Work
              </button>
              <button className="btn secondary" onClick={() => setActiveSection('contact')}>
                Get In Touch
              </button>
            </div>
          </div>
          <div className="hero-visual">
            <div className="profile-card">
              <div className="profile-placeholder">
                {profilePhoto ? (
                  <img src={profilePhoto} alt="Profile" className="profile-photo" />
                ) : (
                  <span className="profile-icon">JD</span>
                )}
              </div>
              <label className="profile-upload-label" htmlFor="hero-profile-upload">
                {profilePhoto ? 'Update Profile Photo' : 'Upload Profile Photo'}
              </label>
              <input
                id="hero-profile-upload"
                type="file"
                accept="image/*"
                className="profile-upload"
                onChange={handlePhotoChange}
              />
              {profilePhotoName && <p className="profile-upload-name">{profilePhotoName}</p>}
            </div>
            <div className="code-animation">
              <div className="code-line">const developer = &#123;</div>
              <div className="code-line indent">name: 'Justin',</div>
              <div className="code-line indent">skills: ['Python', 'React', 'PostgreSQL'],</div>
              <div className="code-line indent">experience: '3 years',</div>
              <div className="code-line indent">passionate: true</div>
              <div className="code-line">&#125;;</div>
            </div>
          </div>
        </div>
      </section>

      <section className={`section about-section ${activeSection === 'about' ? 'active' : ''}`}>
        <div className="section-header">
          <h2>About Me</h2>
          <div className="section-divider"></div>
        </div>
        <div className="about-content">
          <div className="about-text">
            <p>
              I build modern software solutions that automate processes, improve productivity, and create meaningful digital experiences.
              My work is centered around clarity, reliability, and delivering high-quality results.
            </p>
            <p>
              I combine backend strength with frontend polish to deliver applications that are robust, intuitive, and trusted by users.
              I’m committed to standard software practices, secure architecture, and clean delivery.
            </p>
            <div className="about-quote">
              <blockquote>
                "Code is poetry written in logic. Every function tells a story, every algorithm solves a problem."
              </blockquote>
              <cite>- Justin, Software Developer</cite>
            </div>
            <div className="about-details">
              <div className="detail-section">
                <h3>Education & Certifications</h3>
                <ul>
                  <li>AWS Certified Developer</li>
                  <li>React Developer Certification</li>
                  <li>Continuous learning in emerging technologies</li>
                </ul>
              </div>
              <div className="detail-section">
                <h3>Development Philosophy</h3>
                <ul>
                  <li>Write maintainable, scalable code</li>
                  <li>Follow SOLID principles and clean architecture</li>
                  <li>Implement comprehensive testing strategies</li>
                  <li>Focus on performance optimization</li>
                  <li>Embrace agile development methodologies</li>
                </ul>
              </div>
              <div className="detail-section">
                <h3>Work Approach</h3>
                <ul>
                  <li>Collaborative problem-solving</li>
                  <li>Regular code reviews and feedback</li>
                  <li>Documentation-driven development</li>
                  <li>Continuous integration and deployment</li>
                  <li>User-centered design principles</li>
                </ul>
              </div>
            </div>
            <div className="stats">
              <div className="stat">
                <span className="stat-number">3+</span>
                <span className="stat-label">Years Experience</span>
              </div>
              <div className="stat">
                <span className="stat-number">5+</span>
                <span className="stat-label">Projects Completed</span>
              </div>
              <div className="stat">
                <span className="stat-number">9/10</span>
                <span className="stat-label">Average Quality Rating</span>
              </div>
            </div>
            <div className="trust-grid">
              {trustPoints.map((point) => (
                <div key={point.title} className="trust-card">
                  <span className="trust-icon">{point.icon}</span>
                  <h4>{point.title}</h4>
                  <p>{point.detail}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="about-image">
            <div className="about-card">
              <h3>What I Deliver</h3>
              <p>
                Reliable applications, strong security models, and interfaces that make complex processes feel effortless.
              </p>
              <ul>
                <li>Automated finance workflows</li>
                <li>Robust data-driven systems</li>
                <li>Responsive web and desktop workflows</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className={`section projects-section ${activeSection === 'projects' ? 'active' : ''}`}>
        <div className="section-header">
          <h2>My Projects</h2>
          <div className="section-divider"></div>
        </div>
        <div className="projects-intro">
          <p>
            Here are some of my recent projects that showcase my expertise in full-stack development,
            automation, and user experience design. Each project represents a unique challenge solved
            with modern technologies and best practices.
          </p>
          <div className="projects-stats">
            <div className="project-stat">
              <span className="stat-number">50K+</span>
              <span className="stat-label">Lines of Code</span>
            </div>
            <div className="project-stat">
              <span className="stat-number">15+</span>
              <span className="stat-label">Technologies Used</span>
            </div>
            <div className="project-stat">
              <span className="stat-number">100%</span>
              <span className="stat-label">Client Satisfaction</span>
            </div>
          </div>
        </div>
        <div className="projects-grid">
          {projects.map((project, index) => (
            <div key={index} className="project-card">
              <div className="project-icon">{project.icon}</div>
              <h3 className="project-title">{project.title}</h3>
              <p className="project-description">{project.description}</p>
              <div className="project-tech">
                {project.tech.map((tech) => (
                  <span key={tech} className="tech-tag">{tech}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="projects-cta">
          <p>Interested in working together? Let's discuss your next project!</p>
          <button className="btn primary" onClick={() => setActiveSection('contact')}>
            Start a Conversation
          </button>
        </div>
      </section>

      <section className={`section skills-section ${activeSection === 'skills' ? 'active' : ''}`}>
        <div className="section-header">
          <h2>Technical Skills</h2>
          <div className="section-divider"></div>
        </div>
        <div className="skills-content">
          <div className="skills-intro">
            <p>
              I work with a modern stack of technologies to build efficient and dependable applications.
            </p>
            <div className="skills-quote">
              <p>"Technology is best when it brings people together."</p>
              <cite>- Matt Mullenweg</cite>
            </div>
          </div>
          <div className="skills-grid">
            {skills.map((skill) => (
              <div key={skill.name} className="skill-item">
                <div className="skill-header">
                  <span className="skill-icon">{skill.icon}</span>
                  <span className="skill-name">{skill.name}</span>
                </div>
                <div className="skill-bar">
                  <div className="skill-fill" style={{ width: `${skill.level}%` }}></div>
                </div>
                <span className="skill-percentage">{skill.level}%</span>
              </div>
            ))}
          </div>
          <div className="skills-additional">
            <h3>Additional Expertise</h3>
            <div className="additional-skills">
              <span className="skill-tag">Git & Version Control</span>
              <span className="skill-tag">RESTful APIs</span>
              <span className="skill-tag">Database Design</span>
              <span className="skill-tag">UI/UX Design</span>
              <span className="skill-tag">Agile Methodology</span>
              <span className="skill-tag">Cloud Deployment</span>
              <span className="skill-tag">Testing & QA</span>
              <span className="skill-tag">Performance Optimization</span>
            </div>
          </div>
        </div>
      </section>

      <section className={`section contact-section ${activeSection === 'contact' ? 'active' : ''}`}>
        <div className="section-header">
          <h2>Get In Touch</h2>
          <div className="section-divider"></div>
        </div>
        <div className="contact-content">
          <div className="contact-info">
            <p>
              I’m available for new projects and collaborations. Reach out to discuss how I can help bring your next idea to life.
            </p>
            <div className="contact-benefits">
              <h3>Why Work With Me?</h3>
              <ul>
                <li>✓ Dedicated project timeline adherence</li>
                <li>✓ Transparent communication throughout</li>
                <li>✓ Post-launch support and maintenance</li>
                <li>✓ Competitive pricing with quality guarantee</li>
                <li>✓ Modern tech stack and best practices</li>
              </ul>
            </div>
            <div className="contact-availability">
              <h4>Current Availability</h4>
              <p>Available for freelance projects and full-time opportunities</p>
              <p>Response time: Within 24 hours</p>
            </div>
            <div className="contact-methods">
              <div className="contact-method">
                <span className="contact-icon">📧</span>
                <div>
                  <h4>Email</h4>
                  <p>justchuks5@gmail.com</p>
                </div>
              </div>
              <div className="contact-method">
                <span className="contact-icon">💼</span>
                <div>
                  <h4>LinkedIn</h4>
                  <p>https://www.linkedin.com/in/justin-egwuasi-409755340/</p>
                </div>
              </div>
              <div className="contact-method">
                <span className="contact-icon">🐙</span>
                <div>
                  <h4>GitHub</h4>
                  <p>https://github.com/justchuks23/Justchks-git</p>
                </div>
              </div>
            </div>
          </div>
          <div className="contact-form">
            <form className="form">
              <div className="form-group">
                <input type="text" placeholder="Your Name" className="form-input" />
              </div>
              <div className="form-group">
                <input type="email" placeholder="Your Email" className="form-input" />
              </div>
              <div className="form-group">
                <textarea placeholder="Your Message" className="form-textarea" rows="5"></textarea>
              </div>
              <button type="submit" className="btn primary">Send Message</button>
            </form>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-content">
          <p>© 2026 Justin. All rights reserved.</p>
          <p>Built with React & Vite</p>
        </div>
      </footer>
    </div>
  )
}

export default App
