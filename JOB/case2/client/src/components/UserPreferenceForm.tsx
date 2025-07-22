import React, { useState } from 'react';

const AMENITIES = ['Pool', 'Garage', 'Garden'];
const COMMUTE_OPTIONS = [
  { label: '< 15 min', value: 15 },
  { label: '15-30 min', value: 30 },
  { label: '30-45 min', value: 45 },
  { label: '45+ min', value: 60 },
];

type Props = {
  onSubmit: (values: any) => void;
  initialValues?: any;
};

export default function UserPreferenceForm({ onSubmit, initialValues = {} }: Props) {
  const [form, setForm] = useState({
    budget: initialValues.budget || '',
    location: initialValues.location || '',
    min_bedrooms: initialValues.min_bedrooms || 1,
    max_commute: initialValues.max_commute || 30,
    school_rating: initialValues.school_rating || 5,
    amenities: initialValues.amenities || [],
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    const { name, value, type } = e.target;
    if (type === 'checkbox' && e.target instanceof HTMLInputElement) {
      const { checked } = e.target;
      setForm((prev) => ({
        ...prev,
        amenities: checked
          ? [...prev.amenities, value]
          : prev.amenities.filter((a: string) => a !== value),
      }));
    } else {
      setForm((prev) => ({ ...prev, [name]: type === 'number' ? Number(value) : value }));
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit(form);
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md p-4 border rounded bg-white shadow text-gray-800">
      <label>
        Budget ($):
        <input type="number" name="budget" value={form.budget} onChange={handleChange} required className="input" />
      </label>
      <label>
        Location:
        <input type="text" name="location" value={form.location} onChange={handleChange} required className="input" />
      </label>
      <label>
        Minimum Bedrooms:
        <input type="number" name="min_bedrooms" value={form.min_bedrooms} min={1} onChange={handleChange} required className="input" />
      </label>
      <label>
        Max Commute Time:
        <select name="max_commute" value={form.max_commute} onChange={handleChange} className="input">
          {COMMUTE_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      </label>
      <label>
        Minimum School Rating: {form.school_rating}
        <input type="range" name="school_rating" min={1} max={10} value={form.school_rating} onChange={handleChange} className="w-full" />
      </label>
      <fieldset className="flex gap-4">
        <legend>Key Amenities:</legend>
        {AMENITIES.map((amenity) => (
          <label key={amenity} className="flex items-center gap-1">
            <input
              type="checkbox"
              name="amenities"
              value={amenity}
              checked={form.amenities.includes(amenity)}
              onChange={handleChange}
            />
            {amenity}
          </label>
        ))}
      </fieldset>
      <button type="submit" className="btn-primary">Find Properties</button>
    </form>
  );
} 