import mongoose from 'mongoose';
import bcrypt from 'bcrypt';

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, "Name is required"]
    },
    username: {
        type: String,
        required: [true, "Username is required"],
        unique: true
    },
    password: {
        type: String,
        required: [true, "Password is required"],
        minLength: [6, "Password must be at least 6 characters"]
    },
    email: {
        type: String,
        required: [true, "Email is required"],
        unique: true,
        lowercase: true,
        trim: true
    },
    role: {
        type: String,
        enum: ['admin', 'customer'],
        default: 'customer'
    },
    cartItems: [
        {
            quantity: {
                type: Number,
                default: 1
            },
            product:{
                type: mongoose.Schema.Types.ObjectId,
                ref: 'Product'
            }
        }
    ]
},{
    timestamps: true
})

const User = mongoose.model("User", userSchema)

// pre-save hook to hash password before saving to database
userSchema.pre('save', async function(next) {
    if(!this.isModified('password')) return next()
    
    try {
        const salt = await bcrypt.genSalt(10)
        this.password = await bcrypt.hash(this.password, salt)
        next()
    } catch (error) {
        next("error in bcrypt",error)
    }
})

userSchema.methods.comparePassword = async function (password){
    return bcrypt.compare(password, this.password)
}

export default User
