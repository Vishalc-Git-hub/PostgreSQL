
-- 1. USERS TABLE


CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,               
    email VARCHAR(255) UNIQUE NOT NULL,       
    password_hash VARCHAR(255) NOT NULL,      
    first_name VARCHAR(100) NOT NULL,         
    last_name VARCHAR(100) NOT NULL,          
    profile_picture_url VARCHAR(500),         
    bio TEXT,                                 
    headline VARCHAR(255),                    
    user_type VARCHAR(20) NOT NULL
        CHECK (user_type IN ('student', 'instructor', 'both', 'admin')),
    is_active BOOLEAN DEFAULT TRUE,          
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- 2. CATEGORIES TABLE

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,                    
    name VARCHAR(100) UNIQUE NOT NULL,                 
    description TEXT,                                  
    parent_category_id INTEGER REFERENCES categories(category_id),  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP      
);



-- 3. COURSES TABLE


CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,                           
    instructor_id INTEGER NOT NULL REFERENCES users(user_id), 
    category_id INTEGER REFERENCES categories(category_id),   
    title VARCHAR(255) NOT NULL,                            
    subtitle VARCHAR(255),                                  
    description TEXT,                                       
    language VARCHAR(50) DEFAULT 'English',                 
    level VARCHAR(20)
        CHECK (level IN ('Beginner', 'Intermediate', 'Advanced', 'All Levels')),
    price DECIMAL(10, 2) DEFAULT 0.00,                      
    thumbnail_url VARCHAR(500),                             
    promo_video_url VARCHAR(500),                           
    is_published BOOLEAN DEFAULT FALSE,                     
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- 4. SECTIONS TABLE

CREATE TABLE sections (
    section_id SERIAL PRIMARY KEY,                     
    course_id INTEGER NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,                       
    description TEXT,                                  
    order_index INTEGER NOT NULL,                      
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- 5. LECTURES TABLE

CREATE TABLE lectures (
    lecture_id SERIAL PRIMARY KEY,                        
    section_id INTEGER NOT NULL REFERENCES sections(section_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,                          
    description TEXT,                                     
    video_url VARCHAR(500),                               
    duration_seconds INTEGER,                             
    order_index INTEGER NOT NULL,                         
    is_preview BOOLEAN DEFAULT FALSE,                     
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- 6. RESOURCES TABLE

CREATE TABLE resources (
    resource_id SERIAL PRIMARY KEY,                       
    lecture_id INTEGER NOT NULL REFERENCES lectures(lecture_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,                          
    file_url VARCHAR(500) NOT NULL,                       
    file_type VARCHAR(50),                                
    file_size_kb INTEGER,                                
);


-- 7. ENROLLMENTS TABLE

CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,                          
    user_id INTEGER NOT NULL REFERENCES users(user_id),         
    course_id INTEGER NOT NULL REFERENCES courses(course_id),   
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        
    price_paid DECIMAL(10, 2),                                  
    progress_percentage DECIMAL(5, 2) DEFAULT 0.00,             
    completed_at TIMESTAMP,                                     
    UNIQUE(user_id, course_id)                                  
);




-- 8. LECTURE_PROGRESS TABLE

CREATE TABLE lecture_progress (
    progress_id SERIAL PRIMARY KEY,                           
    enrollment_id INTEGER NOT NULL REFERENCES enrollments(enrollment_id) ON DELETE CASCADE,
    lecture_id INTEGER NOT NULL REFERENCES lectures(lecture_id),
    is_completed BOOLEAN DEFAULT FALSE,                       
    last_watched_second INTEGER DEFAULT 0,                    
    completed_at TIMESTAMP,                                   
    UNIQUE(enrollment_id, lecture_id)                        
);



-- 9. REVIEWS TABLE

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,                              
    enrollment_id INTEGER NOT NULL REFERENCES enrollments(enrollment_id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5), 
    comment TEXT,                                               
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(enrollment_id)                                       
);



-- 10. CART_ITEMS TABLE

CREATE TABLE cart_items (
    cart_item_id SERIAL PRIMARY KEY,                         
    user_id INTEGER NOT NULL REFERENCES users(user_id),       
    course_id INTEGER NOT NULL REFERENCES courses(course_id), 
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,             
    UNIQUE(user_id, course_id)                                
);



-- 11. CERTIFICATES TABLE

CREATE TABLE certificates (
    certificate_id SERIAL PRIMARY KEY,                         -- Unique ID for each certificate
    enrollment_id INTEGER NOT NULL REFERENCES enrollments(enrollment_id) ON DELETE CASCADE,
    certificate_url VARCHAR(500),                              -- Link to the generated certificate
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,              -- When it was issued
    UNIQUEQUE(enrollment_id)                                       -- One certificate per enrollment
);